from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from rest_framework.generics import RetrieveUpdateAPIView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin 
from .models import Post, Profile
from .serializers import UserSerializer
from .forms import UserUpdateForm, ProfileUpdateForm, CustomUserCreationForm

User = get_user_model()

# Create your views here.
def home(request):
    return render(request, 'blog/home.html')

class SignupView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'

# CRUD FUNCTIONS
class PostsCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('posts-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date'] 

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_details.html'
    context_object_name = 'post'

    def get_object(self):
        return super().get_object()
    
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_update.html'
    success_url= reverse_lazy('posts-list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect(f"{reverse_lazy('login')}?next={self.request.path}")
        messages.error(self.request, 'You dont  have permissions to edit this post')
        return redirect('post-detail', pk=self.kwargs['pk'])
       

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name ='blog/post_delete.html'
    success_url = reverse_lazy('posts-list')
    context_object_name = 'post'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return redirect(f"{reverse_lazy('login')}?next={self.request.path}")
        messages.error(self.request, 'You dont  have permissions to delete this post')
        return redirect('post-detail', pk=self.kwargs['pk'])


    
class UserProfileView(RetrieveUpdateAPIView):
    model = User
    fields = '__all__'
    serializer_class = UserSerializer
    
    def get_object(self):
        # Return the current authenticated user instead of a queryset
        return self.request.user

# FIXED PROFILE VIEW
@login_required
def profile(request):  # Changed from Profile to profile (lowercase)
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        # Fixed indentation - this should be inside the POST block
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