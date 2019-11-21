from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm
# Create your views here.
def index(request):
    User = get_user_model()
    users = User.objects.all()
    context = {
        'users': users
    }
    return render(request,'accounts/index.html', context)

def log_in(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('accounts:index')
    else:
        form = AuthenticationForm()
    context = {
        'form' : form
    }
    return render(request, 'accounts/form.html', context)

def log_out(request):
    auth_logout(request)
    return redirect('accounts:index')

def signup(request):
    if request.user.is_authenticated:
        return redirect('accounts:index')
    if request.method =='POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('accounts:index')
    else:
        form = CustomUserCreationForm()
    context= {
        'form' : form
    }
    return render(request, 'accounts/form.html', context)

def user(request, user_pk):
    User = get_user_model()
    user = get_object_or_404(User, pk=user_pk)
    context=  {
        'user' : user
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def follow(request, user_pk):
    User = get_user_model()
    follower = get_object_or_404(User, pk=user_pk)
    if request.user in follower.followers.all():
        follower.followers.remove(request.user)
    else:
        follower.followers.add(request.user)
    return redirect('accounts:profile', user_pk)