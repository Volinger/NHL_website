from django.db import models

# Create your models here.


class TableState(models.Model):

    table_name = models.CharField(max_length=256, unique=True)
    last_update = models.DateTimeField()

    def update_table_state(self, table_name, start_time):
        record = self.objects.filter(table_name=table_name).first()
        record.last_update = start_time
        record.save()

class Seasons(models.Model):

    season = models.IntegerField(unique=True)
    games = models.IntegerField()

    def get_current(self):
        current_season = self.objects.all()[-1:]
        return current_season['season']

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
