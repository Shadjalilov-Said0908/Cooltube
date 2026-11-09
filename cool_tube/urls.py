from django.urls import path
from .views import *

urlpatterns = [
    # path('', main_page_view, name='main'),
    # path('category/<int:pk>/', contents_by_category, name='category'),
    # path('content/<int:pk>/', content_detail_view, name='detail'),
    # path('login/', login_user_view, name='login'),
    # path('add/content/', content_create_view, name='add_content')


    path('', MainContentListView.as_view(), name='main'),
    path('category/<int:pk>/', ContentByCategory.as_view(), name='category'),
    path('content/<int:pk>/', ContentDetailView.as_view(), name='detail'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', logout_user_view, name='logout'),
    path('registration/', register_user_view, name='register'),
    path('add/content/', ContentCreateView.as_view(), name='add_content'),
    path('comment/save/<int:pk>/', comment_save, name='comment_save'),
    path('comment/update/<int:pk>/', CommentUpdateView.as_view(), name='comment_update'),
    path('comment/delete/<int:pk>/', comment_delete_view, name='comment_delete'),
    path('search/', SearchContent.as_view(), name='search'),
    path('profile/user/<int:pk>/', profile_user_view, name='profile'),
    path('content/update/<int:pk>/', ContentUpdateView.as_view(), name='content_update'),
    path('content/delete/<int:pk>/', content_delete_view, name='content_delete'),
]




