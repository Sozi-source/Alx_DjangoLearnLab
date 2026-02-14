from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, ListView
from django.views import generic
from .models import Post, User, Profile
from rest_framework.generics import RetrieveUpdateAPIView
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, ProfileSerializer
from .forms import CustomUserCreationForm

User = get_user_model()

# Create your views here.
def home(request):
    return render(request, 'home.html')

class SignupView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'

class PostsCreateView(CreateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('posts-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class PostListView(ListView):
    model =Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date'] 

class PostDetailView(DetailView):
    model= Post
    template_name = 'blog/post_details.html'
    context_object_name = 'post'

    def get_object(self):
        return super().get_object()
    
       

class UserProfileView(RetrieveUpdateAPIView):
    model = User
    fields = '__all__'
    serializer_class = UserSerializer
    
    def get_object(self):
        # Return the current authenticated user instead of a queryset
        return self.request.user

class ProfileView(RetrieveUpdateAPIView):
    model = Profile
    fields ='__all__'
    serializer_class = ProfileSerializer
