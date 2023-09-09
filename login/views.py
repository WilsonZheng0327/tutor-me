from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from student.models import Student
from tutor.models import Tutor
from .models import User

# Create your views here.
def check_auth(request):
    user:User = request.user
    if user.is_authenticated:
        return redirect('/auth')
    else:
        return render(request, "login/index.html")




def login(request):
    user:User = request.user
    if not user.is_authenticated: redirect('')
    if user.user_type == 'student':
        return redirect('student:dashboard')
    elif user.user_type == 'tutor':
        if user.tutor!=None and user.tutor.profile_complete:
            return redirect('tutor:dashboard')
        return redirect('tutor:profile')
    else:
        return redirect('/create')
    
