from django.db import models
from user.models import User
from book.models import Book
from django.utils import timezone



class Loan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    loanDate = models.DateTimeField(default=timezone.now)
    expireDate = models.DateTimeField(default=timezone.now)
    returnDate = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(null=True, max_length=300)