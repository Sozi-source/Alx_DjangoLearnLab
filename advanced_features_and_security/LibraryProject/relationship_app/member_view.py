from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

def is_member(user):
    return user.is_authenticated and user.profile.role =='MEMBER'

@user_passes_test(is_member)
def member_view(request):
    return render(request, 'member_view.html ')