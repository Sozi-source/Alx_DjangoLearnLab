# bookshelf/forms.py
from django import forms
from .models import Book

class ExampleForm(forms.Form):
    """Example form as required by checker"""
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea)

class BookForm(forms.ModelForm):
    """Secure form for Book model with validation"""
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
        widgets = {
            'publication_year': forms.NumberInput(attrs={
                'min': 1900, 
                'max': 2100,
                'placeholder': 'e.g., 2024'
            }),
        }
    
    def clean_title(self):
        """Validate title"""
        title = self.cleaned_data.get('title')
        if len(title) < 2:
            raise forms.ValidationError("Title must be at least 2 characters")
        return title.strip()
    
    def clean_author(self):
        """Validate author"""
        author = self.cleaned_data.get('author')
        if len(author) < 2:
            raise forms.ValidationError("Author must be at least 2 characters")
        return author.strip()
    
    def clean_publication_year(self):
        """Validate publication year"""
        year = self.cleaned_data.get('publication_year')
        if year < 1900 or year > 2100:
            raise forms.ValidationError("Publication year must be between 1900 and 2100")
        return year