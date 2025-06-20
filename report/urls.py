from django.urls import path
from .views import ReportAPIView, MostPopularBookAPIView, UnreturnedBookListAPIView, ExpiredBookListAPIView, MostBorrowerAPIView


urlpatterns = [
    path('report/', ReportAPIView.as_view(), name="report"),
    path('report/most-popular-book/', MostPopularBookAPIView.as_view(), name="most-popular-books"),
    path('report/unreturned-book/', UnreturnedBookListAPIView.as_view(), name="unreturned-books"),
    path('report/expired-book/', ExpiredBookListAPIView.as_view(), name="expired-books"),
    path('report/most-borrowers/', MostBorrowerAPIView.as_view(), name="most-borrowers"),
]