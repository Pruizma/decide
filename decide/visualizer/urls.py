from django.urls import path

from .views import VisualizerView
from .views import VisualizerViewPointsInclude
from .views import StatisticsView
from .views import get_list_votings

urlpatterns = [
    path('<int:voting_id>/', VisualizerView.as_view()),
    path('<int:voting_id>/statistics', StatisticsView.as_view()),
    path('', get_list_votings),
    path('<int:voting_id>/functions', VisualizerViewPointsInclude.as_view())
]
