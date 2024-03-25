from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions, status
from .serializer import ExerciseSerializer, WorkoutPlanSerializer, ProgressSerializer, UserSerializer
from workout_plans.models import Exercise, WorkoutPlan, Progress
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

@swagger_auto_schema(
    method='get',
    operation_summary="Get All Exercises",
    operation_description="This endpoint retrieves a list of all exercises available.",
    responses={
        200: "OK. Returns a list of all exercises.",
        401: "Unauthorized. User is not authenticated.",
        403: "Forbidden. User does not have permission to access this resource.",
    }
)
@api_view(['GET'])
def exercises(request):
    all_exercise = Exercise.objects.all()
    serializer = ExerciseSerializer(all_exercise, many=True)
    return Response(serializer.data)

@swagger_auto_schema(
    method='get',
    operation_summary="Get Single Exercise",
    operation_description="This endpoint retrieves details of a single exercise by its ID.",
    responses={
        200: "OK. Returns details of the requested exercise.",
        404: "Not Found. The requested exercise does not exist.",
    }
)
@api_view(['GET'])
def exercise(request, pk):
    try:
        single_exercise = Exercise.objects.get(id=pk)
        serializer = ExerciseSerializer(single_exercise)
        return Response(serializer.data)
    except Exercise.DoesNotExist:
        return Response({"error": "exercise not found"}, status=status.HTTP_404_NOT_FOUND)

@swagger_auto_schema(
    method='post',
    operation_summary="Create Workout Plan",
    operation_description="This endpoint allows authenticated users to create a new workout plan.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING),
            'description': openapi.Schema(type=openapi.TYPE_STRING),
            'duration': openapi.Schema(type=openapi.TYPE_INTEGER, format=openapi.FORMAT_INT32, description="Duration of the workout plan in days."),
            'goal': openapi.Schema(type=openapi.TYPE_STRING),
            'frequency': openapi.Schema(type=openapi.TYPE_INTEGER, format=openapi.FORMAT_INT32, description="Number of times the workout should be done per week."),
            'daily_session_duration': openapi.Schema(type=openapi.TYPE_INTEGER, format=openapi.FORMAT_INT32, description="Duration of each workout session in minutes."),
        },
        required=['name', 'description', 'duration', 'goal', 'frequency', 'daily_session_duration'],
    ),
    responses={
        201: "Created. Returns the created workout plan data.",
        400: "Bad Request. Returned if the provided data is invalid.",
        401: "Unauthorized. User is not authenticated.",
    }
)
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_workout_plan(request):
    if request.method == 'POST':
        serializer = WorkoutPlanSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='post',
    operation_summary="Create Fitness Progress Entry",
    operation_description="This endpoint allows authenticated users to track their fitness progress.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'date': openapi.Schema(type=openapi.FORMAT_DATE, description="Date of the progress entry."),
            'weight': openapi.Schema(type=openapi.TYPE_NUMBER, format="decimal", description="Current weight in kilograms."),
            'target_weight': openapi.Schema(type=openapi.TYPE_NUMBER, format="decimal", description="Target weight in kilograms."),
            'fitness_goals': openapi.Schema(type=openapi.TYPE_STRING, nullable=True, description="Fitness goals or achievements."),
        },
        required=['date', 'weight', 'target_weight', 'fitness_goals'],
    ),
    responses={
        201: "Created. Returns the created progress data.",
        400: "Bad Request. Returned if the provided data is invalid.",
    }
)
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def progress(request):
    if request.method == 'POST':
        data = request.data
        data['profile'] = request.user.profile.id

        serializer = ProgressSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@swagger_auto_schema(
    method='post',
    operation_summary="User Registration",
    operation_description="This endpoint allows users to register with their information.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=['username', 'password'],
    ),
    responses={
        201: "Created. Returns the created user data.",
        400: "Bad Request. Returned if the provided data is invalid.",
    }
)
@api_view(['POST'])
def user_registration(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='post',
    operation_summary="User Login",
    operation_description="This endpoint allows users to log in.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=['username', 'password'],
    ),
    responses={
        200: "OK. Returns authentication tokens upon successful login.",
        401: "Unauthorized. Returned if the provided credentials are invalid.",
    }
)
@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": "invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )

@swagger_auto_schema(
    method='post',
    operation_summary="Logout",
    operation_description="This endpoint allows authenticated users to log out.",
    responses={
        200: "OK. User logged out successfully.",
        401: "Unauthorized. User is not authenticated.",
    }
)
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)

@swagger_auto_schema(
    method='post',
    operation_summary="Create Profile",
    operation_description="This endpoint allows authenticated users to create their profile.",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'gender': openapi.Schema(type=openapi.TYPE_STRING),
            'age': openapi.Schema(type=openapi.TYPE_INTEGER),
            'height': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_DOUBLE),
            'weight': openapi.Schema(type=openapi.TYPE_NUMBER, format=openapi.FORMAT_DOUBLE),
            'fitness_level': openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=['username', 'gender', 'age', 'height', 'weight', 'fitness_level'],
    ),
    responses={
        201: "Created. Returns the created profile data.",
        400: "Bad Request. Returned if the provided data is invalid.",
        401: "Unauthorized. User is not authenticated.",
    }
)
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_profile(request):
    if request.method == 'POST':
        user = request.user
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





