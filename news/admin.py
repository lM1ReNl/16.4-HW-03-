from django.contrib import admin

from .models import Author, Post, Category, PostCategory, Comment


def nullify_rating(modeladmin, request, queryset):
    queryset.update(rating=0)

nullify_rating.short_description = 'Обнулить рейтинг'

def rating_boost(modeladmin, request, queryset):
    queryset.update(rating=100)

rating_boost.short_description = 'Рейтинг 100!!!'


class CatInLine(admin.TabularInline):
    model = PostCategory
    extra = 1

class PostAdmin(admin.ModelAdmin):
    model = Post
    inlines = (CatInLine,)
    list_display = ('title', 'creation_date', 'type', 'author', 'rating', 'low_rating')
    list_filter = ('title', 'rating', 'creation_date', 'author')
    search_fields = ('title', 'author__full_name', 'creation_date')
    actions = [nullify_rating, rating_boost]


class CatAdmin(admin.ModelAdmin):
    search_fields = (
        'name',
    )
    list_filter = ('name', 'subscribers')


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'rating', 'user')
    list_filter = ('full_name', 'rating', 'user')
    search_fields = ('full_name', 'rating', 'user__username')
    actions = [nullify_rating, rating_boost]

class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ('post', 'category')

class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = [field.name for field in Comment._meta.get_fields()]
    list_filter = ('rating', 'comment_timedate', 'post__title', 'user')
    search_fields = ('text', 'rating', 'comment_timedate', 'post__title', 'user__username')
    actions = [nullify_rating, rating_boost]


admin.site.register(Author, AuthorAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CatAdmin)
admin.site.register(PostCategory, PostCategoryAdmin)
admin.site.register(Comment, CommentAdmin)

