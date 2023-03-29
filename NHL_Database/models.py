"""
Order of tables here defines scraping order. This is not correct - if table A which depends upon table B
would be placed higher, it would be scraped first and this would result in incorrect data being scraped.
# TBD - implement proper table dependency in form of configuration which will define scraping order.
"""

from django.db import models
from django.apps import apps



class TableState(models.Model):

    model_name = models.CharField(max_length=256, unique=True)
    last_update = models.DateTimeField(null=True)

    @staticmethod
    def update_table_state(model_name, last_update):
        record = TableState.objects.filter(model_name=model_name).first()
        record.last_update = last_update
        record.save()

    @staticmethod
    def init_tables():
        app_name = 'NHL_Database'
        models_to_skip = ['TableState']
        app_models = apps.get_app_config(app_name).get_models()
        seen_models = []
        for model in app_models:
            seen_models = seen_models + [model._meta.object_name]
        current_models = [model['model_name'] for model in TableState.objects.values('model_name')]
        missing_models = [model for model in seen_models if model not in current_models]
        missing_models = [model for model in missing_models if model not in models_to_skip]
        for model in missing_models:
            new_table = TableState()
            new_table.model_name = model
            new_table.save()

class Seasons(models.Model):

    season = models.IntegerField(unique=True)
    games = models.IntegerField()

    @staticmethod
    def get_current():
        current_season = Seasons.objects.all().order_by('-season')[0]
        return current_season.season

class Teams(models.Model):

    team = models.CharField(max_length=256)
    firstYearOfPlay = models.IntegerField()
    active = models.BooleanField()


class Teamstats(models.Model):

    season = models.ForeignKey('Seasons', to_field='season', on_delete=models.CASCADE)
    team = models.ForeignKey('Teams', on_delete=models.CASCADE)
    gamesPlayed = models.IntegerField()
    pts = models.IntegerField()
    ptPctg = models.FloatField()
    goalsPerGame = models.FloatField()
    goalsAgainstPerGame = models.FloatField()
    evGGARatio = models.FloatField()
    powerPlayPercentage = models.FloatField()
    powerPlayGoals = models.IntegerField()
    powerPlayGoalsAgainst = models.IntegerField()
    powerPlayOpportunities = models.IntegerField()
    penaltyKillPercentage = models.FloatField()
    shotsPerGame = models.FloatField()
    shotsAllowed = models.FloatField()
    winScoreFirst = models.FloatField()
    winOppScoreFirst = models.FloatField()
    winLeadFirstPer = models.FloatField()
    winLeadSecondPer = models.FloatField()
    winOutshootOpp = models.FloatField()
    winOutshotByOpp = models.FloatField()
    faceOffsTaken = models.IntegerField()
    faceOffsWon = models.IntegerField()
    faceOffsLost = models.IntegerField()
    faceOffWinPercentage = models.FloatField()
    shootingPctg = models.FloatField()
    savePctg = models.FloatField()


class Players(models.Model):

    primaryPosition = models.CharField(max_length=256)
    nationality = models.CharField(max_length=256)
    firstName = models.CharField(max_length=256)
    lastName = models.CharField(max_length=256)


class SkaterSeasonStats(models.Model):

    season = models.ForeignKey('Seasons', to_field='season', on_delete=models.CASCADE)
    player = models.ForeignKey('Players', on_delete=models.CASCADE)
    team = models.ForeignKey('Teams', on_delete=models.CASCADE)
    timeOnIce = models.FloatField(null=True)
    assists = models.IntegerField(null=True)
    goals = models.IntegerField(null=True)
    pim = models.IntegerField(null=True)
    shots = models.IntegerField(null=True)
    games = models.IntegerField(null=True)
    hits = models.IntegerField(null=True)
    powerPlayGoals = models.IntegerField(null=True)
    powerPlayPoints = models.IntegerField(null=True)
    powerPlayTimeOnIce = models.FloatField(null=True)
    evenTimeOnIce = models.FloatField(null=True)
    penaltyMinutes = models.IntegerField(null=True)
    faceOffPct = models.FloatField(null=True)
    shotPct = models.FloatField(null=True)
    gameWinningGoals = models.IntegerField(null=True)
    overTimeGoals = models.IntegerField(null=True)
    shortHandedGoals = models.IntegerField(null=True)
    shortHandedPoints = models.IntegerField(null=True)
    shortHandedTimeOnIce = models.FloatField(null=True)
    blocked = models.IntegerField(null=True)
    plusMinus = models.IntegerField(null=True)
    points = models.IntegerField(null=True)
    shifts = models.IntegerField(null=True)
