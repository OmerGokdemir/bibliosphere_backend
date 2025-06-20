from django.db import models
from django_use_email_as_username.models import BaseUser, BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils import timezone


SCORE = (
    (2,'5 book, 20 days'),
    (1,'4 book, 15 days'), 
    (0,'3 book, 10 days'),   
    (-1,'2 book, 6 days'), 
    (-2,'1 book, 3 days'), 
)


class User(BaseUser):
    firstName=models.CharField(max_length=30)
    lastName=models.CharField(max_length=30)
    score = models.IntegerField(default=0, choices=SCORE)
    address=models.CharField(max_length=100)
    phone=models.CharField(
        max_length=12,
        validators=[
            RegexValidator(
                regex=r'^\d{3}-\d{3}-\d{4}$',
                message='Format must be 999-999-9999'
            )
        ])
    birthDate = models.DateField(blank=True, null=True)
    createDate = models.DateTimeField(default=timezone.now)
    resetPasswordCode = models.CharField(null=True, max_length=255)
    builtIn=models.BooleanField(default=False)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.firstName} {self.lastName}"

    def clean(self):
        if len(self.firstName) < 2:
            raise ValidationError('firstName must be at least 2 characters long.')
        if len(self.lastName) < 2:
            raise ValidationError('lastName must be at least 2 characters long.')
        if len(self.address) < 10:
            raise ValidationError('address must be at least 10 characters long.')
        if len(self.email) < 10:
            raise ValidationError('email must be at least 10 characters long.')

    objects = BaseUserManager()