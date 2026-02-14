from django.db import models
from django.contrib.auth.models import User
from django.conf import settings 


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateField(auto_now_add=True)
    author = models.ForeignKey( settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='posts')

    def __str__(self):
        return self.title
    

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')

    bio = models.TextField(max_length=500, null=True, blank=True)
    location = models.CharField(max_length=50, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profile/', null=True, blank=True)
    
    def __str__(self):
        return self.user.username
    