"""
Initial migration for the game app.

This migration creates the Player, GameSession and DailyAggregate tables
along with their indexes. It is equivalent to what would be generated
via ``python manage.py makemigrations`` for the initial state of the
models defined in ``models.py``.
"""
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='GameSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('started_at', models.DateTimeField()),
                ('ended_at', models.DateTimeField(blank=True, null=True)),
                ('score', models.PositiveIntegerField(default=0)),
                ('duration', models.DurationField(blank=True, null=True)),
                ('hits', models.PositiveIntegerField(default=0)),
                ('combos', models.PositiveIntegerField(default=0)),
                ('device_info', models.CharField(blank=True, max_length=255)),
                ('ip_hash', models.CharField(editable=False, max_length=64)),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sessions', to='game.player')),
            ],
            options={
                'ordering': ['-score', 'ended_at'],
            },
        ),
        migrations.CreateModel(
            name='DailyAggregate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(unique=True)),
                ('best_score', models.PositiveIntegerField(default=0)),
                ('avg_score', models.FloatField(default=0.0)),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.AddIndex(
            model_name='gamesession',
            index=models.Index(fields=['-score', 'ended_at'], name='game_gamesession_score_ended_idx'),
        ),
        migrations.AddIndex(
            model_name='gamesession',
            index=models.Index(fields=['ended_at'], name='game_gamesession_ended_at_idx'),
        ),
        migrations.AddIndex(
            model_name='player',
            index=models.Index(fields=['name'], name='game_player_name_idx'),
        ),
    ]