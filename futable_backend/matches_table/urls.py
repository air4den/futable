from django.urls import path
from .views import MatchListAPIView

urlpatterns = [
    path('matches/<str:league>/<str:season>/', 
         MatchListAPIView.as_view(),
         name='matches_league_season')
]