from django.urls import path, include
from .models import Book
from .views import BookList
from rest_framework import routers
from .views import BookViewSet
from rest_framework.authtoken.views import obtain_auth_token
from .views import CustomAuthToken

router = routers.DefaultRouter()
router.register(r'books_all', BookViewSet, basename='books_all')

urlpatterns= [
    path('books/', BookList.as_view(), name='book-list'),
    path('', include(router.urls)),
    path('api-auth/', CustomAuthToken.as_view(), name='api_token_auth')
]