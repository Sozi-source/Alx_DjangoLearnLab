from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import SignupView
from . import views
from .models import Post
urlpatterns= [
    path('login/', LoginView.as_view(template_name= 'registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', SignupView.as_view(template_name= 'registration/register.html'), name='register'),
    path('home/', views.home, name='home'),
    path('posts/', views.PostListView.as_view(), name='posts-list'),
    path('posts/new/', views.PostsCreateView.as_view(), name='posts-create'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),

]
