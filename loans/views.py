from datetime import timedelta
from django.utils import timezone
from .filters import LoanFilter
from .serializers import LoanSerializer, BookLoanSerializer, BookUserLoanSerializer, UserLoanSerializer
from .models import Loan
from rest_framework.permissions import IsAdminUser, SAFE_METHODS, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework import status


########################################################################

class ListPagination(PageNumberPagination):
    page_size_query_param = 'size'

class IsAdminOrReadOnly(IsAdminUser):
    def has_permission(self, request, view):
        is_admin = super().has_permission(request, view)
        return bool(request.method in SAFE_METHODS or is_admin)

########################################################################



class LoanListAPIView(ListAPIView):
    serializer_class = UserLoanSerializer
    pagination_class = ListPagination
    filterset_class = LoanFilter
    ordering_fields = ['loanDate']
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        queryset = Loan.objects.filter(user=self.request.user)

        sort = self.request.GET.get('sort')
        order = self.request.GET.get('order', 'asc')

        if sort and order:
            if order == 'desc':
                sort = '-' + sort
            queryset = queryset.order_by(sort)
            
        filterset = self.filterset_class(self.request.GET, queryset=queryset)
            
        return filterset.qs

    permission_classes = [IsAuthenticated]



class LoanRetrieveAPIView(RetrieveAPIView):
    serializer_class = UserLoanSerializer

    def get_queryset(self):
        queryset = Loan.objects.filter(user=self.request.user)
        return queryset
    


class UserLoanListAPIView(ListAPIView):
    serializer_class = UserLoanSerializer
    pagination_class = ListPagination
    filterset_class = LoanFilter
    ordering_fields = ['loanDate']
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        user_id = self.kwargs['pk']
        queryset = Loan.objects.filter(user=user_id)

        sort = self.request.GET.get('sort')
        order = self.request.GET.get('order', 'asc')

        if sort and order:
            if order == 'desc':
                sort = '-' + sort
            queryset = queryset.order_by(sort)
            
        filterset = self.filterset_class(self.request.GET, queryset=queryset)
            
        return filterset.qs

    permission_classes = [IsAdminUser]



class BookLoanListAPIView(ListAPIView):
    serializer_class = BookLoanSerializer
    pagination_class = ListPagination
    filterset_class = LoanFilter
    ordering_fields = ['loanDate']
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        book_id = self.kwargs['pk']
        queryset = Loan.objects.filter(book=book_id)

        sort = self.request.GET.get('sort', 'name')
        order = self.request.GET.get('order', 'asc')

        if sort and order:
            if order == 'desc':
                sort = '-' + sort
            queryset = queryset.order_by(sort)
            
        filterset = self.filterset_class(self.request.GET, queryset=queryset)
            
        return filterset.qs

    permission_classes = [IsAdminUser]



class BookUserLoanListAPIView(ListAPIView):
    serializer_class = BookUserLoanSerializer

    def get_queryset(self):
        loan_id = self.kwargs['pk']
        queryset = Loan.objects.filter(id=loan_id)
        return queryset

    permission_classes = [IsAdminUser]



class LoanCreateAPIView(CreateAPIView):
    serializer_class = LoanSerializer
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        book = serializer.validated_data['book']
        user = serializer.validated_data['user']

        if not book.loanable:
            return Response({'isAvailable': False}, status=status.HTTP_400_BAD_REQUEST)

        if Loan.objects.filter(user=user, expireDate__lt=timezone.now(), returnDate__isnull=True).exists():
            return Response({'detail': 'User can not borrow any book as they have overdue books'},
                            status=status.HTTP_400_BAD_REQUEST)

        if user.score >= 2:
            user.score =2
            user.save()
            max_books = 5
            loan_period = 20
        elif user.score == 1:
            max_books = 4
            loan_period = 15
        elif user.score == 0:
            max_books = 3
            loan_period = 10
        elif user.score == -1:
            max_books = 2
            loan_period = 6
        else:
            user.score = -2
            user.save()
            max_books = 1
            loan_period = 3

        if Loan.objects.filter(user=user,returnDate=None).count() >= max_books:
            return Response({'detail': 'User has reached the maximum limit of borrowed books'},
                            status=status.HTTP_400_BAD_REQUEST)

        expire_date = timezone.now() + timedelta(days=loan_period)
        serializer.save(user=user, expireDate=expire_date)

        book.loanable = False
        book.returnDate = None
        book.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)



class LoanUpdateAPIView(UpdateAPIView):
    serializer_class = LoanSerializer
    queryset = Loan.objects.all()
    permission_classes = [IsAdminUser]

    def update(self, request, *args, **kwargs):
        loan = self.get_object()
        serializer = self.get_serializer(loan, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
    
        return_date = serializer.validated_data.get('returnDate')
        notes = serializer.validated_data.get('notes')
        expire_date = serializer.validated_data.get('expireDate')

        if return_date is not None:
            loan.book.loanable = True
            loan.book.save()

            loan.returnDate = return_date
            loan.save()

            time_difference = return_date - loan.expireDate

            user = loan.user
            if time_difference <= timedelta(days=0):
                user.score += 1
            else:
                user.score -= 1
            user.save()

        if notes is not None:
            loan.notes = notes
        if expire_date is not None:
            loan.expireDate = expire_date
        loan.save()

        return Response(serializer.data, status=status.HTTP_200_OK)