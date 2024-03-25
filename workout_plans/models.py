from django.db import models
from users.models import Profile

# Create your models here.
class Exercise(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    sets = models.PositiveIntegerField()
    reps = models.PositiveIntegerField()
    rest_time = models.PositiveIntegerField(help_text="rest time between sets in seconds")
    target_muscle = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class WorkoutPlan(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.PositiveIntegerField(help_text="duration of the workout plan in days")
    goal = models.CharField(max_length=200)    
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    frequency = models.PositiveIntegerField(help_text="workout should be done per week")
    daily_session_duration = models.PositiveIntegerField(help_text="duration of each workout session in minutes")

    exercises = models.ManyToManyField(Exercise, related_name='workout_plans')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Progress(models.Model):
    date = models.DateField()
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    target_weight = models.DecimalField(max_digits=5, decimal_places=2)
    fitness_goals = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    exercise_achievements = models.ManyToManyField(Exercise, related_name='progress_achievements', blank=True)

    def __str__(self):
        return f"{self.profile.user.username} - {self.date}"




