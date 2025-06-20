from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=80)
    builtIn = models.BooleanField(default=False)
    sequence = models.IntegerField(default=1)

    def clean(self):
        if len(self.name) < 2:
            raise ValidationError('Name must be at least 2 characters long.')
        
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['sequence']

@receiver(pre_save, sender=Category)
def set_sequence_value(sender, instance, **kwargs):
    if not instance.pk:
        # If this is a new Category instance
        max_sequence = Category.objects.aggregate(models.Max('sequence'))['sequence__max']
        instance.sequence = max_sequence + 1 if max_sequence is not None else 1



class Author(models.Model):
    name = models.CharField(max_length=70)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    biography = models.TextField()
    builtIn = models.BooleanField(default=False)

    def clean(self):
        if len(self.name) < 4:
            raise ValidationError('Name must be at least 4 characters long.')
    
    def __str__(self):
        return self.name



class Publisher(models.Model):
    name = models.CharField(max_length=50)
    builtIn = models.BooleanField(default=False)   

    def clean(self):
        if len(self.name) < 2:
            raise ValidationError('Name must be at least 2 characters long.') 
    
    def __str__(self):
        return self.name



class Book(models.Model):
    name = models.CharField(max_length=80)
    isbn = models.CharField(
        max_length=17,
        null=False,
        validators=[
            RegexValidator(
                regex=r'^\d{3}-\d{2}-\d{5}-\d{2}-\d$',
                message='Format must be 999-99-99999-99-9'
            )
        ]
    )
    pageCount = models.IntegerField(null=True)
    authorId = models.ManyToManyField(Author)
    publisherId = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    publishDate = models.IntegerField(
        null=True,
        validators=[
            RegexValidator(
                regex=r'^\d{4}$',
                message='Format must be 2023'
            )
        ]
    )
    categoryId = models.ManyToManyField(Category)
    image = models.ImageField(upload_to='images/', null=True)
    loanable = models.BooleanField(default=True)
    shelfCode = models.CharField(
        null=False,
        max_length=6,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z]{2}-\d{3}$',
                message='Format must be AA-999'
            )
        ]
    )
    active = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    createDate = models.DateTimeField(default=timezone.now)
    builtIn = models.BooleanField(default=False)

    def clean(self):
        if len(self.name) < 2:
            raise ValidationError('Name must be at least 2 characters long.')
        
    def __str__(self):
        return self.name