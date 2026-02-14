from django.db import models
from django.contrib.auth.models import User
from django.conf import settings 
from taggit.managers import TaggableManager

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateField(auto_now_add=True)
    author = models.ForeignKey( settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='posts')
   
   # Taggit manager - handles all tag functionality automatically
    tags = TaggableManager(blank=True)

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
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(null=True, blank=True)
    created_at = models.DateField(null=True, blank=True)
    updated_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.post
    
class Tag(models.Model):
    name = models.CharField(max_length=200)
    posts = models.ManyToManyField(Post, related_name='Tags', blank=True)
    created_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name