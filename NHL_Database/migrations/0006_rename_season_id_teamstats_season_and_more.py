# Generated by Django 4.1.7 on 2023-03-14 19:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('NHL_Database', '0005_alter_seasons_season_alter_teamstats_season_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='teamstats',
            old_name='season_id',
            new_name='season',
        ),
        migrations.RenameField(
            model_name='teamstats',
            old_name='team_id',
            new_name='team',
        ),
    ]