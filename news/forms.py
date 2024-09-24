from django import forms
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from allauth.account.forms import SignupForm
# from django.forms import ModelForm

from .models import Post, Author


class PostForm(forms.ModelForm):
    title = forms.CharField(min_length=10)
    text = forms.CharField(min_length=20)

    class Meta:
        model = Post
        fields = [
            'category',
            'title',
            'text',
        ]

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("text")
        title = cleaned_data.get("title")

        if text == title:
            raise ValidationError(
                "Текст не должен быть идентичным названию."
            )

        return cleaned_data


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)
    class Meta:
        model = Author
        exclude = ('rating', 'user')




