from django.urls import path
from .views import RegisterView, LoginView, AuthanticatedUserDetailAPIView, UserLoansListAPIView, UserListCreateAPIView, UserUpdateDeleteRetrieveAPIView,ChangePasswordView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('signin/', LoginView.as_view(), name='signin'),
    path('loans/', UserLoansListAPIView.as_view(), name='user-loans'),
    path('', AuthanticatedUserDetailAPIView.as_view(), name='user'),
    path('users/', UserListCreateAPIView.as_view(), name='users'),
    path('users/<int:pk>/', UserUpdateDeleteRetrieveAPIView.as_view(), name='user-detail'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]