from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.views.generic import FormView
from django.contrib import auth

from .models import UserProfile, Question, Answer


class LoginForm(forms.ModelForm):
    login = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_login(self):
        login = self

    class Meta:
        model = User
        fields = ('login', 'password',)


class UserRegistrationForm(forms.Form):
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="E-mail", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    avatar = forms.ImageField(label='Загрузите аватар', widget=forms.FileInput)

    class Meta:
        model = UserProfile
        fields = ('username', 'email')


class AskForm(forms.Form):
    title = forms.CharField(label='Вопрос', widget=forms.TextInput(attrs={'class': 'form-control'}))
    text = forms.CharField(label='Текст вопроса', widget=forms.Textarea(attrs={'class': 'form-control'}))
    tags = forms.CharField(label='Теги', widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Question
        fields = ('title', 'tags')


class AnswerForm(forms.Form):
    text = forms.CharField(label='Текст вопроса', widget=forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}))

    class Meta:
        model = Answer
        fields = ('text')