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
    
    # Post URLs
    path('posts/', views.PostListView.as_view(), name='posts-list'),
    path('post/new/', views.PostsCreateView.as_view(), name='posts-create'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),  
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),  
    
    # Profile
    path('profile/', views.profile, name='profile'),

    # Comment URLs - Improved version
    # List all comments (optional)
    path('comments/', views.CommentListView.as_view(), name='comment-list'),
    
    # Post-specific comments (more intuitive)
    path('post/<int:post_id>/comments/', views.CommentListView.as_view(), name='post-comments'),
    path('post/<int:post_id>/comments/new/', views.CommentCreateView.as_view(), name='comment-create'),
    
    # Individual comment operations
    path('comment/<int:pk>/', views.CommentDetailView.as_view(), name='comment-detail'),
    path('comment/<int:pk>/update/', views.CommentUpdateView.as_view(), name='comment-update'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment-delete'),
]