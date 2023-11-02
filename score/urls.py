from django.urls import path
from .views import ScoreView


urlpatterns = [
    path('', ScoreView.as_view(
        {'post': 'create', 'get': 'list'})),
]
