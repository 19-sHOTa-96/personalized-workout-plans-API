from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
	path('exercises/', views.exercises),
	path('exercise/<str:pk>/', views.exercise),
	path('workout-plans/create/', views.create_workout_plan),
    path('register/', views.user_registration, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),	
]

