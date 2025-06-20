from django.urls import path
from .views import LoanListAPIView, LoanRetrieveAPIView, UserLoanListAPIView, BookLoanListAPIView, BookUserLoanListAPIView, LoanCreateAPIView, LoanUpdateAPIView

urlpatterns = [
    path('loans/', LoanListAPIView.as_view(), name="loan-list"),
    path('loans/<int:pk>', LoanRetrieveAPIView.as_view(), name="loan-detail"),
    path('loans/user/<int:pk>', UserLoanListAPIView.as_view(), name="user-loan-list"),
    path('loans/book/<int:pk>', BookLoanListAPIView.as_view(), name="book-loan-list"),
    path('loans/auth/<int:pk>', BookUserLoanListAPIView.as_view(), name="book-user-loan-list"),
    path('loans/create/', LoanCreateAPIView.as_view(), name="loan-create"),
    path('loans/update/<int:pk>', LoanUpdateAPIView.as_view(), name="loan-update"),
]