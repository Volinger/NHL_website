# Generated by Django 4.1.7 on 2023-03-28 08:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('NHL_Database', '0013_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TableState',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table_name', models.CharField(max_length=256, unique=True)),
                ('last_update', models.DateTimeField()),
            ],
        ),
        migrations.RemoveField(
            model_name='skaterseasonstats',
            name='player_id',
        ),
        migrations.RemoveField(
            model_name='skaterseasonstats',
            name='season_id',
        ),
        migrations.RemoveField(
            model_name='skaterseasonstats',
            name='team_id',
        ),
        migrations.AddField(
            model_name='skaterseasonstats',
            name='player',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='NHL_Database.players'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='skaterseasonstats',
            name='season',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='NHL_Database.seasons', to_field='season'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='skaterseasonstats',
            name='team',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='NHL_Database.teams'),
            preserve_default=False,
        ),
    ]