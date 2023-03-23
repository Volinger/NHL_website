from rest_framework import serializers
from NHL_Database import models


class PlayersSerializer(serializers.ModelSerializer):

    class Meta:

        model = models.Players
        fields = '__all__'


class SkaterSeasonStatsSerializer(serializers.ModelSerializer):
    season = serializers.SlugRelatedField(many=False, slug_field='season', read_only=True, label='Season')
    player = serializers.SlugRelatedField(queryset=models.Players.objects.all(), slug_field='firstName', label='Name')
    player_surname = serializers.StringRelatedField(source='player.lastName', label='Surname')
    team = serializers.SlugRelatedField(many=False, slug_field='team', read_only=True, label="Team")
    games = serializers.IntegerField(label='GP')
    assists = serializers.IntegerField(label='A')
    goals = serializers.IntegerField(label='G')
    points = serializers.IntegerField(label='P')
    plusMinus = serializers.IntegerField(label='+/-')
    shots = serializers.IntegerField(label='SH')
    hits = serializers.IntegerField(label='HIT')
    powerPlayGoals = serializers.IntegerField(label='PPG')
    powerPlayPoints = serializers.IntegerField(label='PPP')
    powerPlayTimeOnIce = serializers.DecimalField(max_digits=None, decimal_places=2, label='PPTOI')
    evenTimeOnIce = serializers.DecimalField(max_digits=None, decimal_places=2, label='EVTOI')
    penaltyMinutes = serializers.IntegerField(label='PIM')
    faceOffPct = serializers.DecimalField(max_digits=None, decimal_places=2, label='FO%')
    shotPct = serializers.DecimalField(max_digits=None, decimal_places=2, label='SH%')
    gameWinningGoals = serializers.IntegerField(label='GWG')
    overTimeGoals = serializers.IntegerField(label='OTG')
    shortHandedGoals = serializers.IntegerField(label='SHG')
    shortHandedPoints = serializers.IntegerField(label='SHP')
    shortHandedTimeOnIce = serializers.DecimalField(max_digits=None, decimal_places=2, label='SHTOI')
    blocked = serializers.IntegerField(label='BLK')
    shifts = serializers.IntegerField(label='SHIFTS')
    timeOnIce = serializers.DecimalField(max_digits=None, decimal_places=2, label='TOI (min)')

    class Meta:

        model = models.SkaterSeasonStats
        exclude = ['id', 'pim']


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
        exclude = ['id', 'winOutshootOpp', 'winOutshotByOpp', 'winLeadSecondPer', 'winLeadFirstPer', 'winOppScoreFirst',
                   'winScoreFirst', 'evGGARatio']
