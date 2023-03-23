from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from NHL_Database import models
from rest_framework import serializers
from Stats import serializers


class StatsViewSet(viewsets.GenericViewSet):

    @action(detail=False, methods=['get'])
    def standings(self, request):
        params = request.query_params
        query = models.Teamstats.objects
        query = self.query_filter_seasons(params, query)
        if 'order' in params:
            query = query.order_by(params['order'])
        records = query.all()[:20]
        data = serializers.TeamStatsSerializer(records, many=True)
        labels = [field.label for field in serializers.TeamStatsSerializer().get_fields().values()]
        content = {'data': data.data, 'labels': labels}
        return Response(data=content, status=status.HTTP_200_OK)

    def query_filter_seasons(self, params, query):
        if 'season_start' in params:
            if 'season_end' in params:
                query = query.filter(season__season__range=(params['season_start'], params['season_end']))
            else:
                query = query.filter(season__season__gte=params['season_start'])
        elif 'season_end' in params:
            query = query.filter(season__season__lte=params['season_end'])
        return query

    @action(detail=False, methods=['get'])
    def skater_stats(self, request):
        params = request.query_params
        query = models.SkaterSeasonStats.objects
        if 'team' in params:
            query = query.filter(team__team=params['team'])
        if 'nationality' in params:
            query = query.filter(player__nationality=params['nationality'])
        if 'position' in params:
            query = query.filter(player__primaryPosition=params['position'])
        query = self.query_filter_seasons(params, query)
        if 'order' in params:
            query = query.order_by(params['order'])
        records = query.all()[:20]
        data = serializers.SkaterSeasonStatsSerializer(records, many=True)
        labels = [field.label for field in serializers.SkaterSeasonStatsSerializer().get_fields().values()]
        content = {'data': data.data, 'labels': labels}
        return Response(data=content, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def player_career(self, request):
        """
        Fetches stats for entire career of selected player.
        :param request: 'player_id': int
        :return:
        """
        params = request.query_params
        records = models.SkaterSeasonStats.objects.filter(player_id=request.query_params['player_id']).all()
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

    @action(detail=False, methods=['get'])
    def team_history(self, request):
        """
        Fetches stats for teams history.
        :param request:
        :return:
        """
        params = request.query_params
        records = models.Teamstats.objects.filter(team__team=params['team']).all()
        data = serializers.TeamStatsSerializer(records, many=True)
        return Response(data=data.data, status=status.HTTP_200_OK)
