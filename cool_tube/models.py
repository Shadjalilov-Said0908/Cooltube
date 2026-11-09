from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=150, unique=True, verbose_name='Названия категории')

    def __str__(self):
        return self.title

    def get_absolute_url(self):  # метод умной ссылки
        return reverse('category', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = 'Категории'


class Content(models.Model):
    title = models.CharField(max_length=250, verbose_name='Названия')
    descr = models.TextField(verbose_name='Описание')
    photo = models.ImageField(upload_to='photos/', verbose_name='Фото')
    video = models.FileField(upload_to='videos/', verbose_name='Видео',
                             validators=[FileExtensionValidator(allowed_extensions=['mp4', 'avi', 'webm', 'mkv'])])
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    views = models.IntegerField(default=0, verbose_name='Просмотры')
    category = models.ManyToManyField(Category, verbose_name='Категории')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):  # метод умной ссылки
        return reverse('detail', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Контент'
        verbose_name_plural = 'Контенты'


class Comment(models.Model):
    text = models.CharField(max_length=500, verbose_name='Текст комментария')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    content = models.ForeignKey(Content, on_delete=models.CASCADE, verbose_name='Контент')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    def __str__(self):
        return f'Комментарий на контент {self.content.title}, от {self.author.username}, id: {self.pk}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    photo = models.ImageField(upload_to='profiles/', null=True, blank=True, verbose_name='Фото')
    banner = models.ImageField(upload_to='banners/', null=True, blank=True, verbose_name='Заставка')
    name = models.CharField(max_length=100, default='Не задано', verbose_name='Название профиля')
    about = models.CharField(max_length=250, verbose_name='Описание', default='не указано')


    def __str__(self):
        return f'Профиль пользователя {self.user.username}'

    def get_photo(self):
        if self.photo:
            return self.photo.url
        else:
            return 'https://avatars.mds.yandex.net/get-yapic/43978/5cPmC00nWg5G50nhQoTL8fCfQU-1/orig'


    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'















