from django.urls import path
from . import views
from .views import list_books, LibraryDetailView, register
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path(
        'list_books/', 
         views.list_books, 
         name='list_books'
         ),

    path(
        'libraryDetails/<int:pk>/', 
        views.LibraryDetailView.as_view(), 
        name='library_details'
        ),

    path(
        'login/', 
        LoginView.as_view(template_name='relationship_app/login.html'),
        name='login'
        ),

    path(
        'register/', 
        views.register,
        name = 'register'
        
        ),

    path(
        'logout/', 
        LogoutView.as_view(
        template_name='relationship_app/logout.html',
        next_page = 'login',
        http_method_names = ['get', 'post']
        ),
        name='logout'
        ),
]