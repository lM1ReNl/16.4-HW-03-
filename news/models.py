from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.urls import reverse
from django import forms
from django.core.cache import cache

class Author(models.Model):
    full_name = models.CharField(max_length=255)
    rating = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def update_rating(self):
        posts_rating = self.posts.aggregate(pr=Coalesce(Sum('rating'), 0)).get('pr')
        comments_rating = self.user.comments.aggregate(cr=Coalesce(Sum('rating'), 0)).get('cr')
        posts_comments_rating = self.posts.aggregate(pcr=Coalesce(Sum('comment__rating'), 0)).get('pcr')

        self.rating = posts_rating * 3 + comments_rating + posts_comments_rating
        self.save()

    def __str__(self):
        return f'{self.full_name}'

    def get_absolute_url(self):
        return reverse('profile_edit', args=[str(self.pk)])

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, blank=True, null=True, related_name='categories') #возможно, categorys (как в админке)


    def __str__(self):
        return f'{self.name}'


class Post(models.Model):
    article = 'AR'
    news = 'NE'
    CONTENTS = [
        (news, 'Новость'),
        (article, 'Статья')
    ]
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    creation_date = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=2, choices=CONTENTS, default=news)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, through='PostCategory')

    @property
    def low_rating(self):
        return self.rating < 0

    def like_post(self):
        self.rating += 1
        self.save()

    def dislike_post(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:50] + '...'

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return f'/news/{self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'post-{self.pk}')


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.category}'

class Comment(models.Model):
    text = models.TextField()
    rating = models.IntegerField(default=0)
    comment_timedate = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')

    def like_comment(self):
        self.rating += 1
        self.save()

    def dislike_comment(self):
        self.rating -= 1
        self.save()


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2",)



