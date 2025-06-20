from django.urls import path
from .views import BookRetrieveUpdateDestroyAPIView, BookListCreateAPIView, PublisherListCreateAPIView, PublisherRetrieveUpdateDestroyAPIView, CategoryListCreateAPIView, CategoryRetrieveUpdateDestroyAPIView, AuthorListCreateAPIView, AuthorRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('book/<int:pk>', BookRetrieveUpdateDestroyAPIView.as_view(), name="book-get-delete-put"),
    path('books', BookListCreateAPIView.as_view(), name="book-list-create"),

    path('publishers/<int:pk>', PublisherRetrieveUpdateDestroyAPIView.as_view(), name="publisher-get-delete-put"),
    path('publishers', PublisherListCreateAPIView.as_view(), name="publisher-list-create"),

    path('categories/<int:pk>', CategoryRetrieveUpdateDestroyAPIView.as_view(), name="category-get-delete-put"),
    path('categories', CategoryListCreateAPIView.as_view(), name="category-list-create"),

    path('authors/<int:pk>', AuthorRetrieveUpdateDestroyAPIView.as_view(), name="author-get-delete-put"),
    path('authors', AuthorListCreateAPIView.as_view(), name="author-list-create"),
]