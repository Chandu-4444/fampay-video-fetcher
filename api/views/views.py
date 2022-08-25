from django.http import JsonResponse
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from api.models import Result
from rest_framework.views import APIView
from django.db.models import Q
from api.serializers import ResultSerializer


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
        query_set = Result.objects.get_queryset().order_by('-publish_time')
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
        query_set = Result.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query),
        ).order_by("-publish_time")

        paginated_data = self.paginate_queryset(query_set, request)
        serializer = ResultSerializer(paginated_data, many=True)
        return self.get_paginated_response(
            serializer.data,
            code=200,
        )
