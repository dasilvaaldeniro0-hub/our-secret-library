from django.contrib import admin
from .models import Book, Purchase, Payment


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'year', 'is_paid', 'price')
    list_filter = ('is_paid', 'year')
    search_fields = ('title', 'author')


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'purchased_at')
    list_filter = ('purchased_at',)
    search_fields = ('user__username', 'book__title')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'phone_number', 'amount', 'status', 'transaction_id', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'book__title', 'phone_number', 'transaction_id')