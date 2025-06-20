from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Count
from book.serializers import BookSerializer
from .serializers import NewBookSerializer, NewUserSerializer , ReportBookSerializer
from .serializers import ReportSerializer
from book.models import Book, Author, Publisher, Category
from rest_framework.permissions import IsAdminUser, AllowAny
from user.models import User
from loans.models import Loan
from django.utils import timezone
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView

########################################################

class CustomPagination(PageNumberPagination):
    page_size_query_param = 'size'
    page_query_param = 'page'
    page = 1
    page_size = 10

########################################################

class ReportAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        book_count = Book.objects.count()
        author_count = Author.objects.count()
        publisher_count = Publisher.objects.count()
        category_count = Category.objects.count()
        loan_count = Loan.objects.count()
        unreturned_books_count = Loan.objects.filter(returnDate__isnull=True).count()
        expired_books_count = Loan.objects.filter(expireDate__lt=timezone.now(), returnDate__isnull=True).count()
        member_count = User.objects.filter(is_staff=False).count()

        report_data = {
            'books': book_count,
            'authors': author_count,
            'publishers': publisher_count,
            'categories': category_count,
            'loans': loan_count,
            'unReturnedBooks': unreturned_books_count,
            'expiredBooks': expired_books_count,
            'members': member_count,
        }

        serializer = ReportSerializer(report_data)
        return Response(serializer.data)



class MostPopularBookAPIView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        amount = int(request.query_params.get('amount', 10))

        popular_books = (
            Loan.objects
            .values('book')
            .annotate(total_loans=Count('book'))
            .order_by('-total_loans')
            .values('book', 'total_loans')[:amount]
        )

        book_ids = [item['book'] for item in popular_books]
        books = Book.objects.filter(id__in=book_ids)

        sorted_books = sorted(books, key=lambda book: book_ids.index(book.id))

        for book in sorted_books:
            book.total_loans = next(item['total_loans'] for item in popular_books if item['book'] == book.id)

        serializer = NewBookSerializer(sorted_books, many=True)

        paginator = CustomPagination()
        paginated_books = paginator.paginate_queryset(serializer.data, request)

        return paginator.get_paginated_response(paginated_books)
    


class UnreturnedBookListAPIView(ListAPIView):
    serializer_class = ReportBookSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        loan_queryset = Loan.objects.filter(returnDate__isnull=True)
        book_ids = loan_queryset.values_list('book_id', flat=True)
        queryset = Book.objects.filter(id__in=book_ids)

        sort = self.request.GET.get('sort', 'name')
        order = self.request.GET.get('order', 'asc')

        if sort and order:
            if order == 'desc':
                sort = '-' + sort
            queryset = queryset.order_by(sort)
            
        return queryset
    


class ExpiredBookListAPIView(ListAPIView):
    serializer_class = ReportBookSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        loan_queryset = Loan.objects.filter(expireDate__lt=timezone.now(), returnDate__isnull=True)
        book_ids = loan_queryset.values_list('book_id', flat=True)
        queryset = Book.objects.filter(id__in=book_ids)

        sort = self.request.GET.get('sort', 'name')
        order = self.request.GET.get('order', 'asc')

        if sort and order:
            if order == 'desc':
                sort = '-' + sort
            queryset = queryset.order_by(sort)
            
        return queryset
    


class MostBorrowerAPIView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        borrowers = (
            Loan.objects
            .values('user')
            .annotate(total_loans=Count('user'))
            .order_by('-total_loans')
            .values('user', 'total_loans')
        )

        user_ids = [item['user'] for item in borrowers]
        users = User.objects.filter(id__in=user_ids)

        sorted_users = sorted(users, key=lambda user: user_ids.index(user.id))

        for user in sorted_users:
            user.total_loans = next(item['total_loans'] for item in borrowers if item['user'] == user.id)

        serializer = NewUserSerializer(sorted_users, many=True)

        paginator = CustomPagination()
        paginated_users = paginator.paginate_queryset(serializer.data, request)

        return paginator.get_paginated_response(paginated_users)