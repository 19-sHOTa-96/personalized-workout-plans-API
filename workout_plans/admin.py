from django.contrib import admin
from .models import Exercise, WorkoutPlan, Progress

# Register your models here.
admin.site.register(Exercise)
admin.site.register(WorkoutPlan)
admin.site.register(Progress)