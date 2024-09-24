from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User, Group
from django.core.cache import cache
from django.http import request
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django_filters.views import FilterView
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm, ProfileForm
from .models import Post, BaseRegisterForm, Author, Category
from .filters import PostFilter
# from .tasks import inform_about_new_post # celery option
# from .tasks import weekly_mailing
# import datetime
# from datetime import date

class PostList(ListView):
    model = Post
    ordering = '-creation_date'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    queryset = Post.objects.all()
    pk_url_kwarg = 'id'

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["id"]}', None)

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["id"]}', obj)

        return obj

class PostSearch(FilterView):
    model = Post
    filterset_class = PostFilter
    template_name = 'search.html'
    context_object_name = 'news'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'news.add_post'
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'
    context_object_name = 'create'
    success_url = reverse_lazy('post_list')
    login_url = reverse_lazy('post_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        if 'news' in self.request.path:
            post.type = 'NE'
        else:
            post.type = 'AR'
        form.instance.author = self.request.user.author
        today = timezone.now()
        limit = today - timezone.timedelta(days=1)
        if len(Post.objects.filter(author=post.author, creation_date__gte=limit)) >= 3:
            return render(self.request, 'cancel_posting.html', {'author': post.author})
        post.save()
        # inform_about_new_post.delay(form.instance.pk) # celery option
        return super().form_valid(form)


class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'news.change_post'
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'news.delete_post'
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'news/index.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class ProfileUpdate(UpdateView):
    permission_required = 'news.change_author'
    form_class = ProfileForm
    model = User
    pk_url_kwarg = 'pk'
    template_name = 'profile_edit.html'
    def form_valid(self, form):
        if form.is_valid():
            form.save()
        return super().form_valid(form)
    success_url = reverse_lazy('post_list')


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
        Author.objects.create(user=user)
    return redirect('/profile/')  # или /news/


class CategoryListView(ListView):
    model = Post
    template_name = 'news/category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-creation_date')  # or 'created_at'
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы успешно подписались на рассылку новостей категории'
    return render(request, 'news/subscribe.html', {'category': category, 'message': message})



