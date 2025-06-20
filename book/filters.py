import django_filters
from .models import Book, Publisher, Author, Category



class BookFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    cat = django_filters.CharFilter(field_name='categoryId', lookup_expr='exact')
    author = django_filters.CharFilter(field_name='authorId', lookup_expr='exact')
    publisher = django_filters.CharFilter(field_name='publisherId', lookup_expr='exact')

    class Meta:
        model = Book
        fields = []


class PublisherFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    class Meta:
        model = Publisher
        fields = []


class AuthorFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    class Meta:
        model = Author
        fields = []


class CategoryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    class Meta:
        model = Category
        fields = []