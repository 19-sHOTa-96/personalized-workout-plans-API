# Generated by Django 5.0.3 on 2024-03-13 12:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('sets', models.PositiveIntegerField()),
                ('reps', models.PositiveIntegerField()),
                ('rest_time', models.PositiveIntegerField(help_text='rest time between sets in seconds')),
                ('target_muscle', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Progress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('weight', models.DecimalField(decimal_places=2, max_digits=5)),
                ('target_weight', models.DecimalField(decimal_places=2, max_digits=5)),
                ('fitness_goals', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('exercise_achievements', models.ManyToManyField(blank=True, related_name='progress_achievements', to='workout_plans.exercise')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.profile')),
            ],
        ),
        migrations.CreateModel(
            name='WorkoutPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('duration', models.PositiveIntegerField(help_text='duration of the workout plan in days')),
                ('goal', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('frequency', models.PositiveIntegerField(help_text='workout should be done per week')),
                ('daily_session_duration', models.PositiveIntegerField(help_text='duration of each workout session in minutes')),
                ('exercises', models.ManyToManyField(related_name='workout_plans', to='workout_plans.exercise')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.profile')),
            ],
        ),
    ]