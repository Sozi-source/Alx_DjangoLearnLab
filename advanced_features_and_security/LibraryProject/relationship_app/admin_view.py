from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

# user views
def is_admin(user):
    return user.is_authenticated and user.userprofile.role =='ADMIN'

@user_passes_test(is_admin)
def admin_view(request):
    return render (request, 'admin_view.html')