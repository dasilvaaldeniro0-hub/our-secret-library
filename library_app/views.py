import uuid
import time

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Book, Purchase, Payment
from .forms import RegisterForm


def book_list(request):
    query = request.GET.get('q')

    books = Book.objects.all().order_by('title')

    if query:
        books = books.filter(title__icontains=query)

    return render(request, 'books.html', {'books': books})


def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if not book.is_paid:
        return render(request, 'book_detail.html', {'book': book})

    if not request.user.is_authenticated:
        return redirect(f'/login/?next=/book/{book.id}/')

    already_bought = Purchase.objects.filter(
        user=request.user,
        book=book
    ).exists()

    if not already_bought:
        return redirect('buy_book', book_id=book.id)

    return render(request, 'book_detail.html', {'book': book})


@login_required
def buy_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if not book.is_paid:
        messages.info(request, 'Este livro é gratuito.')
        return redirect('book_detail', book_id=book.id)

    already_bought = Purchase.objects.filter(
        user=request.user,
        book=book
    ).exists()

    if already_bought:
        messages.success(request, 'Já tens acesso a este livro.')
        return redirect('book_detail', book_id=book.id)

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        phone_number = request.POST.get('phone_number')

        if not payment_method:
            messages.error(request, 'Escolhe o método de pagamento.')
            return redirect('buy_book', book_id=book.id)

        if not phone_number:
            messages.error(request, 'Introduz o número de telefone.')
            return redirect('buy_book', book_id=book.id)

        if payment_method not in ['emola', 'mpesa']:
            messages.error(request, 'Método de pagamento inválido.')
            return redirect('buy_book', book_id=book.id)

        transaction_id = f"{payment_method.upper()}-{uuid.uuid4().hex[:10].upper()}"

        payment = Payment.objects.create(
            user=request.user,
            book=book,
            phone_number=phone_number,
            amount=book.price,
            payment_method=payment_method,
            status='pending',
            transaction_id=transaction_id
        )

        return redirect('process_payment', payment_id=payment.id)

    return render(request, 'buy_book.html', {'book': book})


@login_required
def process_payment(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)

    if payment.user != request.user:
        messages.error(request, 'Não tens permissão para acessar este pagamento.')
        return redirect('book_list')

    if payment.status == 'paid':
        Purchase.objects.get_or_create(
            user=payment.user,
            book=payment.book
        )
        return redirect('book_detail', book_id=payment.book.id)

    time.sleep(2)

    payment.status = 'paid'
    payment.save()

    Purchase.objects.get_or_create(
        user=payment.user,
        book=payment.book
    )

    messages.success(
        request,
        f'Pagamento {payment.get_payment_method_display()} aprovado! Referência: {payment.transaction_id}'
    )

    return redirect('book_detail', book_id=payment.book.id)


def register_view(request):
    if request.user.is_authenticated:
        return redirect('book_list')

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)

            messages.success(request, 'Conta criada com sucesso.')
            return redirect('book_list')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


@login_required
def my_books(request):
    purchases = Purchase.objects.filter(
        user=request.user
    ).select_related('book')

    return render(request, 'my_books.html', {'purchases': purchases})