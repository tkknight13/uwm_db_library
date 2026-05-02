from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False)
    author = models.CharField(max_length=200, null=False, blank=False)
    isbn = models.CharField(max_length=13, null = False, blank=False, unique=True)
    quantity = models.PositiveIntegerField(default=1, null=False, blank=False)

    def __str__(self):
        return self.title
    def is_available(self):
        from .models import Checkout  # local import to avoid circular issues
        checked_out_count = Checkout.objects.filter(book=self).count()
        return checked_out_count < self.quantity


class Checkout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    checked_out_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} → {self.book.title}"