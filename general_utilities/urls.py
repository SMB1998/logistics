from django.urls import path
from .views import LastScrapingDateView

urlpatterns = [
    path('last-scraping-date/', LastScrapingDateView.as_view(), name='last-scraping-date'),
]
