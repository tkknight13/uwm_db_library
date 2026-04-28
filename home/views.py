from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from home.models import Book, Checkout
from .forms import BookForm


def home_view(request):
    return render(request, 'home.html')

def home_redirect(request):
    if request.user.is_authenticated:
        if is_admin(request.user):
            return redirect('admin_home')
        else:
            return redirect('student_home')
    else:
        return render(request, 'home.html')

def is_admin(user):
    return user.is_staff or user.is_superuser


def login_view(request):
    if request.user.is_authenticated:
        if is_admin(request.user):
            return redirect('admin_home')
        else:
            return redirect('student_home')

    if request.method == 'POST':
        username = request.POST.get('username')  # this will be email
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')

            if is_admin(user):
                return redirect('admin_home')
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'login.html')


@login_required(login_url='login')
@user_passes_test(is_admin, login_url='home')
def admin_home(request):
    return render(request, 'admin_home.html')


@login_required(login_url='login')
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')

def signup_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')

        # Basic validation
        if not all([first_name, last_name, email, password, role]):
            messages.error(request, 'All fields are required.')
            return redirect('signup')

        # Check if user already exists
        if User.objects.filter(username=email).exists():
            messages.error(request, 'An account with this email already exists.')
            return redirect('signup')

        # Create user (email used as username)
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        # Optional: make admins staff users
        if role == 'administrator':
            user.is_staff = True
            user.save()

        messages.success(request, 'Account created successfully!')
        return redirect('login')

    return render(request, 'signup.html')


@login_required
def student_home(request):
    borrowed_books = Checkout.objects.filter(user=request.user)
    books = Book.objects.all()

    return render(request, "student_home.html", {
        "borrowed_books": borrowed_books,
        "books": books
    })

def view_books(request):
    books = Book.objects.all()
    return render(request, 'view_books.html', {'books': books})

@login_required
@user_passes_test(is_admin)
def add_book(request):
    form = BookForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('admin_home')

    return render(request, 'book_form.html', {'form': form})


@login_required
@user_passes_test(is_admin)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    form = BookForm(request.POST or None, instance=book)

    if form.is_valid():
        form.save()
        return redirect('admin_home')

    return render(request, 'book_form.html', {'form': form})


@login_required
@user_passes_test(is_admin)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return redirect('admin_home')

@login_required
def checkout_book(request, pk):
    book = get_object_or_404(Book, pk=pk)

    checked_out_count = Checkout.objects.filter(book=book).count()

    if checked_out_count < book.quantity:
        Checkout.objects.create(user=request.user, book=book)

    return redirect('student_home')

@login_required
def return_book(request, pk):
    checkout = get_object_or_404(
        Checkout,
        user=request.user,
        book_id=pk
    )

    checkout.delete()
    return redirect('student_home')