from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('buy/<int:book_id>/', views.buy_book, name='buy_book'),
    path('register/', views.register_view, name='register'),
    path('my-books/', views.my_books, name='my_books'),
    path('process/<int:payment_id>/', views.process_payment, name='process_payment'),
]