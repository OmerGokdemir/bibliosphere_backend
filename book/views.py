from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from .serializers import BookSerializer, PublisherSerializer, CategorySerializer, AuthorSerializer
from .models import Book, Publisher, Category, Author
from rest_framework.permissions import IsAdminUser, SAFE_METHODS, AllowAny
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from .filters import BookFilter, PublisherFilter, CategoryFilter, AuthorFilter
from rest_framework.response import Response
from rest_framework import status


########################################################################

class IsAdminOrReadOnly(IsAdminUser):

    def has_permission(self, request, view):
        is_admin = super().has_permission(request, view)
        return bool(request.method in SAFE_METHODS or is_admin)

class ListPagination(PageNumberPagination):
    page_size_query_param = 'size'

########################################################################


class BookListCreateAPIView(ListCreateAPIView):
    serializer_class = BookSerializer
    filterset_class = BookFilter
    pagination_class = ListPagination
    ordering_fields = ['name',"createDate"]
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = Book.objects.all()

        sort = self.request.GET.get('sort', 'name')
        order = self.request.GET.get('order', 'asc')

        if sort and order:
            if order == 'desc':
                sort = '-' + sort
            queryset = queryset.order_by(sort)
            
        filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return filterset.qs
    
    def create(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().create(request, *args, **kwargs)
        return Response({'message': 'Only Admin can create book'}, status=status.HTTP_401_UNAUTHORIZED)


    


class BookRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    permission_classes = [IsAdminOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        if request.user.is_superuser:
            book = self.get_object()
            if book.loanable == False:
                return Response({
                    'message': 'Book cannot be deleted as it is associated with a loan.',
                    'success': False
                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                pk = book.pk
                book.delete()
                return Response({
                    'message': f'Book-{pk} is deleted successfully',
                    'success': True
                })
        return Response({'message':'Only Admin can delete book'},status=status.HTTP_401_UNAUTHORIZED)
    
    def update(self, request, *args, **kwargs):
        if request.user.is_superuser:
            pk=self.kwargs['pk']
            super().update(request, *args, **kwargs)
            return Response({
                    'message': f'Book-{pk} is updated succesfully','success':True
                })
        else:
            print(request.user)
            return Response({'message': 'Only Admin can update book'}, status=status.HTTP_401_UNAUTHORIZED)





class PublisherRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = PublisherSerializer
    queryset = Publisher.objects.all()

    def destroy(self, request, *args, **kwargs):
        if request.user.is_superuser:
            publisher = self.get_object()

            if Book.objects.filter(publisherId=publisher).exists():
                return Response({'message': 'Can not delete user with pending loans'}, status=status.HTTP_400_BAD_REQUEST)
            
            pk=self.kwargs['pk']
            super().destroy(request, *args, **kwargs)
            return Response({
                'message': f'Publisher-{pk} is deleted succesfully','success':True
            })
        return Response({'message':'Only Admin can delete publisher'},status=status.HTTP_401_UNAUTHORIZED)
    
    def update(self, request, *args, **kwargs):
        if request.user.is_superuser:
            pk=self.kwargs['pk']
            super().update(request, *args, **kwargs)
            return Response({
                    'message': f'Publisher-{pk} is updated succesfully','success':True
                })
        return Response({'message': 'Only Admin can update publisher'}, status=status.HTTP_401_UNAUTHORIZED)

    permission_classes = [IsAdminOrReadOnly]



class PublisherListCreateAPIView(ListCreateAPIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = PublisherSerializer
    pagination_class = ListPagination
    filterset_class = PublisherFilter
    ordering_fields = ['name',"id"]
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        queryset = Publisher.objects.all()

        sort = self.request.GET.get('sort', 'name')
        order = self.request.GET.get('order', 'asc')

        if sort and order:
            if order == 'desc':
                sort = '-' + sort
            queryset = queryset.order_by(sort)
            
        filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return filterset.qs
    
    def create(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().create(request, *args, **kwargs)
        return Response({'message': 'Only Admin can create publisher'}, status=status.HTTP_401_UNAUTHORIZED)
    

    


class AuthorRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()

    def destroy(self, request, *args, **kwargs):
        if request.user.is_superuser:
            author = self.get_object()

            if Book.objects.filter(authorId=author).exists():
                return Response({'message': 'Can not delete user with pending loans'}, status=status.HTTP_400_BAD_REQUEST)
            
            pk=self.kwargs['pk']
            super().destroy(request, *args, **kwargs)
            return Response({
                'message': f'Author-{pk} is deleted succesfully','success':True
            })
        return Response({'message':'Only Admin can delete author'},status=status.HTTP_401_UNAUTHORIZED)
    
    def update(self, request, *args, **kwargs):
        if request.user.is_staff:
            pk=self.kwargs['pk']
            super().update(request, *args, **kwargs)
            return Response({
                    'message': f'Author-{pk} is updated succesfully','success':True
                })
        return Response({'message': 'Only Admin can update author'}, status=status.HTTP_401_UNAUTHORIZED)

    permission_classes = [IsAdminOrReadOnly]



class AuthorListCreateAPIView(ListCreateAPIView):
    serializer_class = AuthorSerializer
    pagination_class = ListPagination
    filterset_class = AuthorFilter
    ordering_fields = ['name']
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        queryset = Author.objects.all()

        sort = self.request.GET.get('sort', 'name')
        order = self.request.GET.get('order', 'asc')

        if sort and order:
            if order == 'desc':
                sort = '-' + sort
            queryset = queryset.order_by(sort)
            
        filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return filterset.qs
    
    def create(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super().create(request, *args, **kwargs)
        return Response({'message': 'Only Admin can create author'}, status=status.HTTP_401_UNAUTHORIZED)

    permission_classes = [IsAdminOrReadOnly]




class CategoryRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def destroy(self, request, *args, **kwargs):
        if request.user.is_superuser:
            category = self.get_object()

            if Book.objects.filter(categoryId=category).exists():
                return Response({'message': 'Can not delete user with pending loans'}, status=status.HTTP_400_BAD_REQUEST)
            
            pk=self.kwargs['pk']
            super().destroy(request, *args, **kwargs)
            return Response({
                'message': f'Category-{pk} is deleted succesfully','success':True
            })
        return Response({'message':'Only Admin can delete category'},status=status.HTTP_401_UNAUTHORIZED)
    
    def update(self, request, *args, **kwargs):
        if request.user.is_staff:
            pk=self.kwargs['pk']
            super().update(request, *args, **kwargs)
            return Response({
                    'message': f'Category-{pk} is updated succesfully','success':True
                })
        return Response({'message': 'Only Admin can update category'}, status=status.HTTP_401_UNAUTHORIZED)

    permission_classes = [IsAdminOrReadOnly]



class CategoryListCreateAPIView(ListCreateAPIView):
    serializer_class = CategorySerializer
    pagination_class = ListPagination
    filterset_class = CategoryFilter
    ordering_fields = ['name']
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        queryset = Category.objects.all()

        sort = self.request.GET.get('sort', 'name')
        order = self.request.GET.get('order', 'asc')

        if sort and order:
            if order == 'desc':
                sort = '-' + sort
            queryset = queryset.order_by(sort)
            
        filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return filterset.qs

    def create(self, request, *args, **kwargs):
        if request.user.is_staff:
            return super().create(request, *args, **kwargs)
        return Response({'message': 'Only Admin can create category'}, status=status.HTTP_401_UNAUTHORIZED)
    
    permission_classes = [IsAdminOrReadOnly]