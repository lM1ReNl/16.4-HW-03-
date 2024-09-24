import django_filters
from django.forms import DateInput
# from django_filters import FilterSet, CharFilter, DateTimeFilter, ModelChoiceFilter, DateFilter

# from . import forms
from .models import Post


class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains', label='Поиск по названию')
    author = django_filters.CharFilter(field_name='author__full_name', lookup_expr='icontains', label='Поиск по автору')
    creation_date = django_filters.DateFilter(field_name='creation_date', lookup_expr='date__gte', label='Позже указанной даты', widget=DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Post
        fields = ['title', 'author', 'creation_date']




