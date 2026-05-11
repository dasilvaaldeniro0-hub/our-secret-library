from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Book


@login_required(login_url='login')
def books(request):
    all_books = Book.objects.all()

    return render(request, 'books.html', {
        'books': all_books
    })


def login_view(request):
    if request.user.is_authenticated:
        return redirect('books')

    error = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('books')
        else:
            error = 'Invalid username or password.'

    return render(request, 'login.html', {
        'error': error
    })


def logout_view(request):
    logout(request)
    return redirect('login')