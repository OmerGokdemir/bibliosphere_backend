from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import AccessToken
from loans.filters import LoanFilter
from rest_framework import serializers
from loans.models import Loan
from loans.serializers import LoanSerializer, LoanSerializerForUser
from user.filters import UserFilter
from .models import User
from .serializers import RegisterSerializer, CustomLoginSerializer, UserSerializer, CreateUserSerializer, UpdateUserSerializer,ChangePasswordSerializer
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, \
    ListCreateAPIView, get_object_or_404, UpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password, check_password

##############################################################################

class ListPagination(PageNumberPagination):
    page_size_query_param = 'size'

##############################################################################



class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
    
        return Response({'message':'Registerisation is successfully done','success':True})
    


class LoginView(TokenObtainPairView):
    serializer_class=CustomLoginSerializer
    
    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data['user']
        access_token=str(AccessToken.for_user(user)) # str AccessToken > api_settings > ACCESS_TOKEN_LIFETIME
        
        return Response({'token':access_token})



class AuthanticatedUserDetailAPIView(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    


class UserLoansListAPIView(ListAPIView):
    serializer_class = LoanSerializerForUser
    pagination_class = ListPagination
    filterset_class = LoanFilter
    ordering_fields = ['createDate']
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        queryset = Loan.objects.filter(user=self.request.user)

        sort = self.request.GET.get('sort',"id")
        order = self.request.GET.get('order', 'asc')

        if sort and order:
            if order == 'desc':
                sort = '-' + sort
            queryset = queryset.order_by(sort)
            
        filterset = self.filterset_class(self.request.GET, queryset=queryset)
            
        return filterset.qs
    
    permission_classes = [IsAuthenticated]



class UserListCreateAPIView(ListCreateAPIView):
    serializer_class = CreateUserSerializer
    pagination_class = ListPagination
    ordering_fields = ['createDate']
    filterset_class = UserFilter
    filter_backends = [DjangoFilterBackend]


    def get_queryset(self):
        queryset = User.objects.all()

        sort = self.request.GET.get('sort', 'id')
        order = self.request.GET.get('order', 'asc')

        if sort and order:
            if order == 'desc':
                sort = '-' + sort
            queryset = queryset.order_by(sort)
            
        filterset = self.filterset_class(self.request.GET, queryset=queryset)
            
        return filterset.qs

    def perform_create(self, serializer):
        user = serializer.save()
        request_user = self.request.user

        if request_user.is_superuser:
            user.save()
        else:
            user.is_staff = False
            user.is_superuser = False

        user.save()

    permission_classes = [IsAdminUser]
    #permission_classes = [AllowAny]


class UserUpdateDeleteRetrieveAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = UpdateUserSerializer
    queryset = User.objects.all()

    def destroy(self, request, *args, **kwargs):
        if request.user.is_superuser:
            user = self.get_object()

            if Loan.objects.filter(user=user, returnDate__isnull=True).exists():
                return Response({'message': 'Can not delete user with pending loans'}, status=status.HTTP_400_BAD_REQUEST)
            
            super().destroy(request, *args, **kwargs)
            return Response({
                'message': f'User-{user.pk} is deleted succesfully','success':True
            })
        return Response({'message':'Only Admin can delete user'},status=status.HTTP_401_UNAUTHORIZED)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if request.user.is_superuser:
            serializer = self.get_serializer(instance, data=request.data, partial=True)

        elif request.user.is_staff and not instance.is_superuser and not instance.is_staff:
            request.data['is_staff'] = False
            request.data['is_superuser'] = False
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            
        else:
            return Response({'message': 'Only Admin or Employee with member-type users can update users'},
                            status=status.HTTP_401_UNAUTHORIZED)

        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    permission_classes = [IsAdminUser]


class ChangePasswordView(APIView):
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data['password']):
                return Response({'message': 'Geçersiz eski parola'}, status=status.HTTP_400_BAD_REQUEST)

            # changePasswordCode' unun geçerliliğini doğrulayın

            newPassword = serializer.validated_data['newPassword']
            user.set_password(newPassword)
            user.save()

            return Response({'message': 'Parola başarıyla değiştirildi.'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)