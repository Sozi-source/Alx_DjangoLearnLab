from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    # Authentication URLs
    path('login/', LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'), 
    path('register/', views.SignupView.as_view(), name='register'),  
    
    # Main pages
    path('home/', views.home, name='home'),
    
    # Post URLs (consistent pattern - all using 'posts/' prefix)
    path('posts/', views.PostListView.as_view(), name='posts-list'),
    path('posts/new/', views.PostsCreateView.as_view(), name='posts-create'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),  
    path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),  
    
    # Profile
    path('profile/', views.profile, name='profile'),
]