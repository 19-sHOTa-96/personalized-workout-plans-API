from rest_framework import serializers
from users.models import Profile
from workout_plans.models import Exercise, WorkoutPlan, Progress
from django.contrib.auth.models import User

class ExerciseSerializer(serializers.ModelSerializer):
	class Meta:
		model = Exercise
		fields = '__all__'

class WorkoutPlanSerializer(serializers.ModelSerializer):
	class Meta:
		model = WorkoutPlan
		fields = '__all__'

class ProgressSerializer(serializers.ModelSerializer):
	class Meta:
		model = Progress
		fields = '__all__'


# User Login/Logout Register
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'






