# stocks/urls.py
from django.urls import path
from .views import DailyPriceDateRangeView

urlpatterns = [
    path('indexes/<int:index_id>/prices/<str:start_date>/<str:end_date>/',
         DailyPriceDateRangeView.as_view(), name='dailyprice-date-range'),
]
