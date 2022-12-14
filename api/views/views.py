from django.http import JsonResponse
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from api.models import Result
from rest_framework.views import APIView
from django.db.models import Q
from django.conf import settings
from api.serializers import ResultSerializer
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


# A custom pagination class to handle pagination for the results.
# A custom pagination class is needed because the default pagination class does not include response code.
class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data, **kwargs):
        return Response({
            'code': kwargs['code'],
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        })


class ResultView(APIView, CustomPagination):
    """
    This method is used to fetch all the results.

    Route: /api/search/?page=<page_number>
    """
    serializer_class = ResultSerializer

    def get(self, request):
        if "fetch_results" in cache:
            print("Results are in cache")
            query_set = cache.get("fetch_results")
        else:
            print("Results are not in cache")
            query_set = Result.objects.get_queryset().order_by('-publish_time')
            cache.set("fetch_results", query_set, CACHE_TTL)

        paginated_data = self.paginate_queryset(query_set, request)
        serializer = ResultSerializer(paginated_data, many=True)
        return self.get_paginated_response(
            serializer.data,
            code=200,
        )


class SearchView(APIView, CustomPagination):
    """
    This method is used to search for results based on the query.
    Route: /api/search/?page=<page_number>&query=<query>
    """
    serializer_class = ResultSerializer

    def get(self, request):
        query = request.GET.get("query")
        if f"{query}_search_results" in cache:
            print("Results are in cache")
            query_set = cache.get(f"{query}_search_results")
        else:
            print("Results are not in cache")
            query_set = Result.objects.filter(
                Q(title__icontains=query) | Q(description__icontains=query),
            ).order_by("-publish_time")
            cache.set(f"{query}_search_results", query_set, CACHE_TTL)

        paginated_data = self.paginate_queryset(query_set, request)
        serializer = ResultSerializer(paginated_data, many=True)
        return self.get_paginated_response(
            serializer.data,
            code=200,
        )
