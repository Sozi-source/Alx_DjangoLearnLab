from rest_framework import serializers
from .models import Post, User, Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 
                 'bio', 'location', 'birth_date', 'profile_picture']
        read_only_fields = ['id', 'username'] 

class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only = True)

    class Meta:
        model=Post
        fields = [
            'id', 
            'title', 
            'content', 
            'author', 
            'author_id',
            'created_date', 
            'published_date', 
            'status'
        ]
        read_only_fields = ['id', 'created_date']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields ='__all__'