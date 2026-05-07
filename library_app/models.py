from django.db import models
from django.contrib.auth.models import User


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    year = models.IntegerField()
    description = models.TextField(blank=True, null=True)
    pdf = models.FileField(upload_to='books/', blank=True, null=True)
    cover = models.ImageField(upload_to='covers/', blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    cover_url = models.URLField(blank=True, null=True)
    pdf_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='purchases')
    purchased_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')
        ordering = ['-purchased_at']

    def __str__(self):
        return f"{self.user.username} comprou {self.book.title}"
    
class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('paid', 'Pago'),
        ('failed', 'Falhou'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    PAYMENT_METHOD_CHOICES = [
    ('emola', 'e-Mola'),
    ('mpesa', 'M-Pesa'),
    ]

    payment_method = models.CharField(
    max_length=20,
    choices=PAYMENT_METHOD_CHOICES,
    default='mpesa'
    )

    def __str__(self):
        return f"Pagamento {self.user.username} - {self.book.title} - {self.status}"