from rest_framework import viewsets
from .models import CustomUser, KYC, Wallet
from .serializers import CustomUserSerializer, KYCSerializer, WalletSerializer, UserRegisterSerializer, LoginSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permisstion_classes = (AllowAny, )
    serializer_class = UserRegisterSerializer


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            user_serializer = UserSerializer(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token), # type: ignore
                'user' : user_serializer.data
            })
        else:
            return Response({'detail': 'Invalid credentials'}, status=401)

class DashboardView(APIView):
    permission_classes = [IsAuthenticated] 
    def get(self, request):
        user = request.user
        user_serializer = UserSerializer(user)
        return Response({
            "message": "Welcome to the dashboard!", 
            "user": user_serializer.data
        }, 200)

class CustomUserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated] 
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class KYCViewSet(viewsets.ModelViewSet):
    queryset = KYC.objects.all()
    serializer_class = KYCSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer