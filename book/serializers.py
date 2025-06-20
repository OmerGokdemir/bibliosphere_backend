from rest_framework import serializers
from .models import Book, Category, Publisher, Author


class BookSerializer(serializers.ModelSerializer):
    authorName = serializers.SerializerMethodField()
    categoryName = serializers.SerializerMethodField()
    publisherName = serializers.SerializerMethodField()

    def get_authorName(self, obj):
        author_names = [author.name for author in obj.authorId.all()]
        return ", ".join(author_names) if author_names else ""

    def get_categoryName(self, obj):
        category_names = [category.name for category in obj.categoryId.all()]
        return ", ".join(category_names) if category_names else ""

    def get_publisherName(self, obj):
        return obj.publisherId.name

    class Meta:
        model = Book
        fields = ["id", "name", "authorName", "categoryName", "publisherName", "image", "pageCount", "isbn", "authorId",
                  "publisherId", "categoryId", "publishDate", "loanable", "shelfCode", "active", "featured",
                  "createDate", "builtIn"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'