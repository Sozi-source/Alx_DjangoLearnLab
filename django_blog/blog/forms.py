from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    """
    Form for updating User model fields
    """
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email']
    
    def clean_email(self):
        """Validate email is unique"""
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError('This email is already in use.')
        return email

class ProfileUpdateForm(forms.ModelForm):
    """
    Form for updating Profile model fields
    """
    class Meta:
        model = Profile
        fields = ['bio', 'location', 'birth_date', 'profile_pic']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Tell us about yourself...'}),
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }