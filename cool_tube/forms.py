from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Content, Comment, Profile


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    password = forms.CharField(label='Пароль',widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))

    error_messages = {
        "invalid_login": "неверный логин или пароль "

    }


class RegisterUserForm(UserCreationForm):  # Форма регистрации
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    password1 = forms.CharField(label='Придумайте пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))

    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))

    first_name = forms.CharField(label='Ваше имя', widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    last_name = forms.CharField(label='Ваша фамилия', widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    email = forms.EmailField(label='Ваша почта', widget=forms.EmailInput(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')


class ContentForm(forms.ModelForm):
    title = forms.CharField(label='Название',  widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    descr = forms.CharField(label='Описание',  widget=forms.Textarea(attrs={
        'class': 'form-control'
    }))

    photo = forms.ImageField(label='Фото контента', widget=forms.FileInput(attrs={
        'class': 'form-control'
    }))

    video = forms.FileField(label='Видео контента', widget=forms.FileInput(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = Content
        fields = ('title', 'descr', 'photo', 'video', 'category')
        widgets = {
            'category': forms.SelectMultiple(attrs={'class': 'form-control'})
        }


class CommentForm(forms.ModelForm):
    text = forms.CharField(label=False, widget=forms.Textarea(attrs={
        'class': 'form-control bg-black text-light comment-input',
        'placeholder': 'Введите комментарий',
        'style': 'height: 30px; border: 0; border-bottom: 1px solid white'
    }))

    class Meta:
        model = Comment
        fields = ('text',)


class ChangeUserForm(forms.ModelForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    first_name = forms.CharField(label='Ваше имя', widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    last_name = forms.CharField(label='Ваша фамилия', widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    email = forms.EmailField(label='Ваша почта', widget=forms.EmailInput(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')


class ChangeProfileForm(forms.ModelForm):
    photo = forms.ImageField(label='Фото', required=False, widget=forms.FileInput(attrs={
        'class': 'form-control'
    }))

    name = forms.CharField(label='Название профиля', max_length=100, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    about = forms.CharField(label='О профиле', max_length=250, required=False, widget=forms.Textarea(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = Profile
        fields = ('name', 'photo', 'about')



class ChangePasswordUserForm(PasswordChangeForm):
    old_password = forms.CharField(label='Текущий пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))

    new_password1 = forms.CharField(label='Новый пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))

    new_password2 = forms.CharField(label='Подтвердить пароль', widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))
