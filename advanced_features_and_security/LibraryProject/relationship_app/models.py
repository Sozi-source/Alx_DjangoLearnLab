# relationship_app/models.py
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

# Import CustomUser from bookshelf app
from bookshelf.models import CustomUser

# Create your models here.
class Author(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    title=models.CharField(max_length=100)
    author=models.ForeignKey(Author, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
    
    class Meta:
        permissions= (
            ("can_add_book", "Can add book"),
            ("can_change_book", "Can change book"),
            ("can_delete_book", "Can delete book"),
        )


class Library(models.Model):
    name= models.CharField(max_length=100)
    books= models.ManyToManyField(Book)

    def __str__(self):
        return self.name


class Librarian(models.Model):
    name = models.CharField(max_length=100)
    library = models.OneToOneField(Library, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    ADMIN = 'Admin'
    LIBRARIAN = 'Librarian'
    MEMBER = 'Member'

    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (LIBRARIAN, 'Librarian'),
        (MEMBER, 'Member'),
    ]
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,  # This will now point to bookshelf.CustomUser
        on_delete=models.CASCADE, 
        related_name='profile'
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=MEMBER)

    def __str__(self):
        return f"{self.user.username}- {self.role}"


# Update the signal receivers to use CustomUser instead of User
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()