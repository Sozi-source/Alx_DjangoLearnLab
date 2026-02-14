from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, ListView
from .models import Post, User, Profile
from rest_framework.generics import RetrieveUpdateAPIView
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, ProfileSerializer
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect

User = get_user_model()

# Create your views here.
def home(request):
    return render(request, 'home.html')

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


@login_required
def Profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

    if user_form.is_valid() and profile_form.is_valid():
        user_form.save()  # Save user data
        profile_form.save()  # Save profile data
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    else:
        # Handle GET request - display forms
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'blog/profile.html', context)