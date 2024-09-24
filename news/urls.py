from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import views
from .views import PostList, PostDetail, PostSearch, PostCreate, PostUpdate, PostDelete, BaseRegisterView, IndexView, \
    upgrade_me, ProfileUpdate, CategoryListView, subscribe

from django.views.decorators.cache import cache_page

urlpatterns = [
    path('news/', cache_page(15)(PostList.as_view()), name='post_list'),
    path('news/<int:id>', cache_page(30)(PostDetail.as_view()), name='post_detail'),
    path('news/search/', PostSearch.as_view(), name='post_search'),
    path('news/create/', PostCreate.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', PostUpdate.as_view(), name='news_edit'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
    path('articles/create/', PostCreate.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', PostUpdate.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', PostDelete.as_view(), name='article_delete'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('signup/', BaseRegisterView.as_view(template_name='signup.html'), name='signup'),
    path('profile/', IndexView.as_view()),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('<int:pk>/edit/', ProfileUpdate.as_view(), name='profile_edit'),
    path('categories/<int:pk>/', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/subscribe/', subscribe, name='subscribe'),
]

