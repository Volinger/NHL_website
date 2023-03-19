from rest_framework import serializers
from NHL_Models import models


class PlayersSerializer(serializers.ModelSerializer):

    class Meta:

        model = models.Players
        fields = '__all__'


class SkaterSeasonStatsSerializer(serializers.ModelSerializer):
    season_id = serializers.IntegerField(label='Season')
    # player_name = serializers.SlugRelatedField(queryset=models.Players.objects.all(), slug_field='firstName', label='Name')
    # player_surname = serializers.SlugRelatedField(queryset=models.Players.objects.all(), slug_field='lastName', label='Last Name')
    # team_id = serializers.SlugRelatedField(many=False, slug_field='team', read_only=True, label="Team")
    timeOnIce = serializers.FloatField(label='TOI')
    assists = serializers.IntegerField(label='A')
    goals = serializers.IntegerField(label='G')
    pim = serializers.IntegerField(label='PIM')
    shots = serializers.IntegerField(label='SH')
    games = serializers.IntegerField(label='GP')
    hits = serializers.IntegerField(label='HIT')
    powerPlayGoals = serializers.IntegerField(label='PPG')
    powerPlayPoints = serializers.IntegerField(label='PPP')
    powerPlayTimeOnIce = serializers.FloatField(label='PPTOI')
    evenTimeOnIce = serializers.FloatField(label='EVTOI')
    penaltyMinutes = serializers.IntegerField(label='PM')
    faceOffPct = serializers.FloatField(label='FO%')
    shotPct = serializers.FloatField(label='SH%')
    gameWinningGoals = serializers.IntegerField(label='GWG')
    overTimeGoals = serializers.IntegerField(label='OTG')
    shortHandedGoals = serializers.IntegerField(label='SHG')
    shortHandedPoints = serializers.IntegerField(label='SHP')
    shortHandedTimeOnIce = serializers.FloatField(label='SHTOI')
    blocked = serializers.IntegerField(label='BLK')
    plusMinus = serializers.IntegerField(label='+/-')
    points = serializers.IntegerField(label='P')
    shifts = serializers.IntegerField(label='SHIFTS')

    class Meta:

        model = models.SkaterSeasonStats
        fields = '__all__'


class SeasonsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Seasons
        fields = '__all__'


class TeamStatsSerializer(serializers.ModelSerializer):
    season = serializers.SlugRelatedField(many=False, slug_field='season', read_only=True, label="Season")
    team = serializers.SlugRelatedField(many=False, slug_field='team', read_only=True, label="Team")
    gamesPlayed = serializers.IntegerField(label='GP')
    pts = serializers.IntegerField(label='P')
    ptPctg = serializers.FloatField(label='P%')
    goalsPerGame = serializers.FloatField(label='G/GP')
    goalsAgainstPerGame = serializers.FloatField(label='GA/GP')
    # evGGARatio = serializers.FloatField(label='')
    powerPlayPercentage = serializers.FloatField(label='PP%')
    powerPlayGoals = serializers.IntegerField(label='PPG')
    powerPlayGoalsAgainst = serializers.IntegerField(label='PPG/A')
    powerPlayOpportunities = serializers.IntegerField(label='PP_opp')
    penaltyKillPercentage = serializers.FloatField(label='PK%')
    shotsPerGame = serializers.FloatField(label='S/G')
    shotsAllowed = serializers.FloatField(label='SA/G')
    # winScoreFirst = serializers.FloatField(label='')
    # winOppScoreFirst = serializers.FloatField(label='')
    # winLeadFirstPer = serializers.FloatField(label='')
    # winLeadSecondPer = serializers.FloatField(label='')
    # winOutshootOpp = serializers.FloatField(label='')
    # winOutshotByOpp = serializers.FloatField(label='')
    faceOffsTaken = serializers.IntegerField(label='FO')
    faceOffsWon = serializers.IntegerField(label='FO_won')
    faceOffsLost = serializers.IntegerField(label='FO_lost')
    faceOffWinPercentage = serializers.FloatField(label='FO%')
    shootingPctg = serializers.FloatField(label='SH%')
    savePctg = serializers.FloatField(label='SV%')


    class Meta:
        model = models.Teamstats
        # fields = '__all__'
        exclude = ['id', 'winOutshootOpp', 'winOutshotByOpp', 'winLeadSecondPer', 'winLeadFirstPer', 'winOppScoreFirst',
                   'winScoreFirst', 'evGGARatio']
