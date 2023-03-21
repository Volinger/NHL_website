# Generated by Django 4.1.7 on 2023-03-15 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NHL_Database', '0009_players'),
    ]

    operations = [
        migrations.CreateModel(
            name='SkaterSeasonStats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('season_id', models.IntegerField()),
                ('player_id', models.IntegerField()),
                ('team_id', models.IntegerField()),
                ('timeOnIce', models.FloatField()),
                ('assists', models.IntegerField()),
                ('goals', models.IntegerField()),
                ('pim', models.IntegerField()),
                ('shots', models.IntegerField()),
                ('games', models.IntegerField()),
                ('hits', models.IntegerField()),
                ('powerPlayGoals', models.IntegerField()),
                ('powerPlayPoints', models.IntegerField()),
                ('powerPlayTimeOnIce', models.FloatField()),
                ('evenTimeOnIce', models.FloatField()),
                ('penaltyMinutes', models.IntegerField()),
                ('faceOffPct', models.FloatField()),
                ('shotPct', models.FloatField()),
                ('gameWinningGoals', models.IntegerField()),
                ('overTimeGoals', models.IntegerField()),
                ('shortHandedGoals', models.IntegerField()),
                ('shortHandedPoints', models.IntegerField()),
                ('shortHandedTimeOnIce', models.FloatField()),
                ('blocked', models.IntegerField()),
                ('plusMinus', models.IntegerField()),
                ('points', models.IntegerField()),
                ('shifts', models.IntegerField()),
            ],
        ),
    ]
