from django.urls import path
from api.views import ResultView, SearchView

urlpatterns = [
    path("fetch/", ResultView.as_view()),
    path("search/", SearchView.as_view()),
]
