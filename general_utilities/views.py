import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

class LastScrapingDateView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        last_scraping_date = os.environ.get('LAST_SCRAPING_DATE', None)
        return Response({
            'last_scraping_date': last_scraping_date
        })
