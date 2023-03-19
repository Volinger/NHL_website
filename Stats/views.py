from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from NHL_Models import models
from rest_framework import serializers
from Stats import serializers
import json
from django.db.models import Avg, Count, Min, Sum


class StatsViewSet(viewsets.GenericViewSet):

    @action(detail=False, methods=['get'])
    def standings(self, request):
        records = models.Teamstats.objects.all()[:20]
        data = serializers.TeamStatsSerializer(records, many=True)
        labels = [field.label for field in serializers.TeamStatsSerializer().get_fields().values()]
        content = {'data': data.data, 'labels': labels}
        return Response(data=content, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def skater_stats(self, request):
        records = models.SkaterSeasonStats.objects.all()[:10]
        data = serializers.SkaterSeasonStatsSerializer(records, many=True)
        labels = [field.label for field in serializers.SkaterSeasonStatsSerializer().get_fields().values()]
        content = {'data': data.data, 'labels': labels}
        return Response(data=content, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def player_career(self, request):
        """
        Fetches stats for entire career of selected player.
        :param request:
        :return:
        """
        player_id = request.query_params['player_id']
        records = models.SkaterSeasonStats.objects.filter(player_id=player_id).all()
        data = serializers.SkaterSeasonStatsSerializer(records, many=True)
        return Response(data=data.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def players(self, request):
        """
        Fetches list of all players.
        :param request:
        :return:
        """
        records = models.Players.objects.all()
        data = serializers.PlayersSerializer(records, many=True)
        return Response(data=data.data, status=status.HTTP_200_OK)
