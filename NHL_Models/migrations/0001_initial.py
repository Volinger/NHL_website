# Generated by Django 4.1.7 on 2023-03-16 19:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Players',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('primaryPosition', models.CharField(max_length=256)),
                ('nationality', models.CharField(max_length=256)),
                ('firstName', models.CharField(max_length=256)),
                ('lastName', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Seasons',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('season', models.IntegerField(unique=True)),
                ('games', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='SkaterSeasonStats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('season_id', models.IntegerField()),
                ('player_id', models.IntegerField()),
                ('team_id', models.IntegerField()),
                ('timeOnIce', models.FloatField(null=True)),
                ('assists', models.IntegerField(null=True)),
                ('goals', models.IntegerField(null=True)),
                ('pim', models.IntegerField(null=True)),
                ('shots', models.IntegerField(null=True)),
                ('games', models.IntegerField(null=True)),
                ('hits', models.IntegerField(null=True)),
                ('powerPlayGoals', models.IntegerField(null=True)),
                ('powerPlayPoints', models.IntegerField(null=True)),
                ('powerPlayTimeOnIce', models.FloatField(null=True)),
                ('evenTimeOnIce', models.FloatField(null=True)),
                ('penaltyMinutes', models.IntegerField(null=True)),
                ('faceOffPct', models.FloatField(null=True)),
                ('shotPct', models.FloatField(null=True)),
                ('gameWinningGoals', models.IntegerField(null=True)),
                ('overTimeGoals', models.IntegerField(null=True)),
                ('shortHandedGoals', models.IntegerField(null=True)),
                ('shortHandedPoints', models.IntegerField(null=True)),
                ('shortHandedTimeOnIce', models.FloatField(null=True)),
                ('blocked', models.IntegerField(null=True)),
                ('plusMinus', models.IntegerField(null=True)),
                ('points', models.IntegerField(null=True)),
                ('shifts', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Teams',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team', models.CharField(max_length=256)),
                ('firstYearOfPlay', models.IntegerField()),
                ('active', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Teamstats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gamesPlayed', models.IntegerField()),
                ('pts', models.IntegerField()),
                ('ptPctg', models.FloatField()),
                ('goalsPerGame', models.FloatField()),
                ('goalsAgainstPerGame', models.FloatField()),
                ('evGGARatio', models.FloatField()),
                ('powerPlayPercentage', models.FloatField()),
                ('powerPlayGoals', models.IntegerField()),
                ('powerPlayGoalsAgainst', models.IntegerField()),
                ('powerPlayOpportunities', models.IntegerField()),
                ('penaltyKillPercentage', models.FloatField()),
                ('shotsPerGame', models.FloatField()),
                ('shotsAllowed', models.FloatField()),
                ('winScoreFirst', models.FloatField()),
                ('winOppScoreFirst', models.FloatField()),
                ('winLeadFirstPer', models.FloatField()),
                ('winLeadSecondPer', models.FloatField()),
                ('winOutshootOpp', models.FloatField()),
                ('winOutshotByOpp', models.FloatField()),
                ('faceOffsTaken', models.IntegerField()),
                ('faceOffsWon', models.IntegerField()),
                ('faceOffsLost', models.IntegerField()),
                ('faceOffWinPercentage', models.FloatField()),
                ('shootingPctg', models.FloatField()),
                ('savePctg', models.FloatField()),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NHL_Models.seasons', to_field='season')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='NHL_Models.teams')),
            ],
        ),
    ]
