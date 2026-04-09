from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect

# Create your views here.
from django.shortcuts import render


@login_required(login_url='login')
def home_view(request):
    return render(request, 'home.html')


def is_admin(user):
    def is_admin(user):
        return user.is_staff or user.is_superuser


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')  # Already logged in, redirect away

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            # Redirect admins to admin home, regular users to home
            if is_admin(user):
                return redirect('admin_home')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')
@login_required(login_url='login')
@user_passes_test(is_admin, login_url='home')
def admin_home(request):
    context = {}
    return render(request, 'admin_home.html', context)


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')

def signup_view(request):
    return render(request, 'signup.html')  # build this out later