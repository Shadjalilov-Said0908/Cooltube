from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Category, Content, Comment, Profile
from .forms import LoginUserForm, RegisterUserForm, ContentForm, CommentForm, ChangeUserForm, ChangeProfileForm, ChangePasswordUserForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q


# Create your views here.
# def main_page_view(request):
#     contents = Content.objects.all().order_by('-created_at')
#     context = {
#         'title': 'CoolTube',
#         'contents': contents
#     }
#
#     return render(request, 'cool_tube/main.html', context)

class MainContentListView(ListView):
    model = Content  # От куда взять все объекты из какой модели
    context_object_name = 'contents'  # Под каким ключом отправим список на html страницу
    template_name = 'cool_tube/main.html'  # Для какой html страницы
    ordering = '-created_at'  # сортировка
    extra_context = {'title': 'CoolTube'}


# ===================================================================================
# def contents_by_category(request, pk):
#     contents = Content.objects.filter(category=pk).order_by('-created_at')
#     category = Category.objects.get(pk=pk)
#     context = {
#         'contents': contents,
#         'title': f'CoolTube: {category.title}'
#     }
#
#     return render(request, 'cool_tube/main.html', context)

class ContentByCategory(MainContentListView):

    def get_queryset(self):  # Метод, что бы переназначить вывод
        contents = Content.objects.filter(category=self.kwargs['pk']).order_by('-created_at')
        return contents

    # Метод при помощи которого можем передать на страницу что то ещё
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        category = Category.objects.get(pk=self.kwargs['pk'])
        context['title'] = f'CoolTube: {category.title}'
        return context


# ===================================================================================
# def content_detail_view(request, pk):
#     content = Content.objects.get(pk=pk)
#     same_contents = Content.objects.filter(category__in=content.category.all()).distinct().exclude(pk=content.pk)
#
#     context = {
#         'title': content.title,
#         'content': content,
#         'same_contents': same_contents
#     }
#
#     return render(request, 'cool_tube/content_detail.html', context)

class ContentDetailView(DetailView):
    model = Content
    context_object_name = 'content'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        content = context['content']
        context['title'] = content.title
        context['same_contents'] = Content.objects.filter(category__in=content.category.all()).distinct().exclude(
            pk=content.pk)
        context['comment_form'] = CommentForm()
        context['comments'] = Comment.objects.filter(content=content).order_by('-created_at')
        return context


# ===================================================================================
# def login_user_view(request):
#     if request.user.is_authenticated:
#         return redirect('main')
#     if request.method == 'POST':
#         form = LoginUserForm(data=request.POST)
#         if form.is_valid():
#             user = form.get_user()  # метод получения пользователя из Бд если пароль и логин верные
#             if user:
#                 login(request, user)
#                 return redirect('main')  # это функция которая перенаправит
#     else:
#         form = LoginUserForm()
#
#     context = {
#         'title': 'Авторизация',
#         'form': form
#     }
#
#     return render(request, 'cool_tube/login.html', context)

class LoginUserView(LoginView):
    form_class = LoginUserForm
    template_name = 'cool_tube/login.html'
    next_page = 'main'
    redirect_authenticated_user = 'main'
    extra_context = {'title': 'Авторизация'}


# ===================================================================================


def logout_user_view(request):
    logout(request)
    return redirect('main')


def register_user_view(request):
    if request.user.is_authenticated:
        return redirect('main')

    if request.method == 'POST':
        form = RegisterUserForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            profile = Profile.objects.create(user=user)
            profile.save()
            return redirect('login')
    else:
        form = RegisterUserForm()

    context = {
        'title': 'Регистрация',
        'form': form
    }
    return render(request, 'cool_tube/register.html', context)


# def content_create_view(request):
#     if request.user.is_authenticated:
#         if request.method == 'POST':
#             # логика сохранения контента
#             form = ContentForm(request.POST, request.FILES)
#             if form.is_valid():
#                 content = form.save(commit=False)  # Подожди не сохраняй
#                 content.author = request.user
#                 content.save()
#                 form.save_m2m()
#                 return redirect('detail', content.pk)
#         else:
#             form = ContentForm()
#
#         context = {
#             'title': 'Добавить контент',
#             'form': form
#         }
#         return render(request, 'cool_tube/content_create.html', context)
#     else:
#         return redirect('login')


class ContentCreateView(LoginRequiredMixin, CreateView):
    form_class = ContentForm
    template_name = 'cool_tube/content_create.html'
    extra_context = {'title': 'Добавить контент'}
    login_url = 'login'

    def form_valid(self, form):  # Метод в котором форм указали кто автор контента
        form.instance.author = self.request.user
        return super(ContentCreateView, self).form_valid(form)


# Функция сохранения комментария
def comment_save(request, pk):
    if request.user.is_authenticated and request.method == 'POST':
        if Content.objects.filter(pk=pk).exists():
            form = CommentForm(data=request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = request.user
                comment.content = Content.objects.get(pk=pk)
                comment.save()
                return redirect('detail', pk)
        else:
            return redirect('main')
    else:
        return redirect('login')


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    form_class = CommentForm
    model = Comment
    login_url = 'login'

    def post(self, request, *args, **kwargs):
        if Comment.objects.filter(pk=self.kwargs['pk'], author=request.user):
            return super(CommentUpdateView, self).post(request, *args, **kwargs)
        else:
            return redirect('main')

    def get_success_url(self):
        comment = Comment.objects.get(pk=self.kwargs['pk'])
        return reverse('detail', kwargs={'pk': comment.content.pk})


def comment_delete_view(request, pk):
    if request.user.is_authenticated:
        if Comment.objects.filter(pk=pk, author=request.user):
            comment = Comment.objects.get(pk=pk)
            comment.delete()
            return redirect('detail', comment.content.pk)
        else:
            return redirect('main')
    else:
        return redirect('login')


class SearchContent(MainContentListView):

    def get_queryset(self):
        word = self.request.GET.get('q')
        contents = Content.objects.filter(
            Q(title__iregex=word) | Q(descr__iregex=word) | Q(author__username__iregex=word))
        return contents.order_by('-created_at')


def profile_user_view(request, pk):
    if User.objects.filter(pk=pk).exists():
        user = User.objects.get(pk=pk)
        profile = Profile.objects.get(user=user)
        contents = Content.objects.filter(author=user)
        context = {
            'title': f'Профиль {user.username}',
            'profile': profile,
            'contents': contents,
            'user_form': ChangeUserForm(instance=user),
            'profile_form': ChangeProfileForm(instance=profile),
            'password_form': ChangePasswordUserForm(request.user)
        }
        return render(request, 'cool_tube/profile.html', context)

    else:
        return redirect('main')


class ContentUpdateView(LoginRequiredMixin, UpdateView):
    model = Content
    form_class = ContentForm
    template_name = 'cool_tube/content_create.html'
    extra_context = {'title': 'Изменить контент'}
    login_url = 'main'

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.request.user.pk})

    def get(self, request, *args, **kwargs):  # Метод проверки на сущ контента и авторство при get запросе
        if Content.objects.filter(pk=self.kwargs['pk'], author=request.user).exists():
            return super(ContentUpdateView, self).get(request, *args, **kwargs)
        else:
            return redirect('main')

    def post(self, request, *args, **kwargs):  # Метод проверки на сущ контента и авторство при post запросе
        if Content.objects.filter(pk=self.kwargs['pk'], author=request.user).exists():
            return super(ContentUpdateView, self).post(request, *args, **kwargs)
        else:
            return redirect('main')


def content_delete_view(request, pk):
    if request.user.is_authenticated:
        if Content.objects.filter(pk=pk, author=request.user).exists():
            content = Content.objects.get(pk=pk)
            content.delete()
            return redirect('profile', request.user.pk)
        else:
            return redirect('main')
    else:
        return redirect('login')
