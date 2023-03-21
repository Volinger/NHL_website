from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from NHL_Database import models
from rest_framework import serializers
from Stats import serializers
from django.db.models import Q

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
        # params = {key: value[0] if len(value) == 1 else value for key, value in request.query_params.items()}
        # params['team__team'] = params.pop('team')
        # query = models.SkaterSeasonStats.objects
        # filters = self.build_optional_filters(params=params, query=query)
        # records = query.get(filters).all()
        params = request.query_params
        query = models.SkaterSeasonStats.objects
        if params['team'] != '-':
            query = query.filter(team__team=params['team'])
        if params['position'] != '-':
            query = query.filter(player__primaryPosition=params['position'])
        records = query.all()[:20]
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
        params = request.query_params
        query = models.SkaterSeasonStats.objects.filter(player_id=request.query_params.id).all()
        query = self.build_optional_filters(params, query)
        records = query.all()
        data = serializers.SkaterSeasonStatsSerializer(records, many=True)
        return Response(data=data.data, status=status.HTTP_200_OK)

    # @staticmethod
    # def build_optional_filters(params, query):
    #     """
    #     Check params and append filter statements to query if they are not empty.
    #     :return:
    #     """
    #     query = Q()
    #     for key in params.keys():
    #         if params[key] != '-':
    #             query &= Q(**{key: params[key]})
    #     return query

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

    @action(detail=False, methods=['get'])
    def seasons(self, request):
        """
        Fetches list of all seasons.
        :param request:
        :return:
        """
        records = models.Seasons.objects.all()
        data = serializers.SeasonsSerializer(records, many=True)
        return Response(data=data.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def positions(self, request):
        """
        Fetches list of skater positions.
        :param request:
        :return:
        """
        records = [item['primaryPosition'] for item in models.Players.objects.values('primaryPosition').distinct()]
        return Response(data=records, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def teams(self, request):
        """
        Fetches list of NHL teams.
        :param request:
        :return:
        """
        records = [item['team'] for item in models.Teams.objects.order_by('team').values('team').distinct()]
        return Response(data=records, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def nationalities(self, request):
        """
        Fetches list of all player's nationalities.
        :param request:
        :return:
        """
        records = [item['nationality'] for item in models.Players.objects.order_by('nationality').values('nationality').distinct()]
        return Response(data=records, status=status.HTTP_200_OK)
