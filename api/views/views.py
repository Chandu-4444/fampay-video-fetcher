import os

from django.conf import settings
from django.http import JsonResponse
from rest_framework.pagination import PageNumberPagination

from api.models import Result
from rest_framework.views import APIView
from fampay.celery import app as celery_app
from django.db.models import Q
from django.conf import settings
from api.serializers import ResultSerializer


class ResultView(APIView, PageNumberPagination):
    serializer_class = ResultSerializer

    def get(self, request):
        query_set = Result.objects.all()
        paginated_data = self.paginate_queryset(query_set, request)
        serializer = ResultSerializer(paginated_data, many=True)
        return self.get_paginated_response(serializer.data)


class SearchView(APIView, PageNumberPagination):
    serializer_class = ResultSerializer

    def get(self, request):
        query = request.GET.get("query")
        query_set = Result.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query),
        ).order_by("-publish_time")

        paginated_data = self.paginate_queryset(query_set, request)
        serializer = ResultSerializer(paginated_data, many=True)
        return self.get_paginated_response(serializer.data)
