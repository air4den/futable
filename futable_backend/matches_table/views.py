from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from rest_framework.views import APIView

from .models import Match
from .serializers import MatchSerializer

class MatchListAPIView(APIView):
    def get(self, request, league, season):
        matches = Match.objects.filter(league=league, season=season)
        serializer = MatchSerializer(matches, context={'request': request}, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

"""
@api_view(['GET'])
def match_list_by_league_season(request, league, season):
    matches = Match.objects.filter(league=league, season=season)
    serializer = MatchSerializer(matches, context={'request': request}, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
"""
