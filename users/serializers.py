from rest_framework import serializers
from .models import CustomUser, KYC, Wallet
from cards.serializers import CardSerializer
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_active', 'date_joined']

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    
    def create(self, validated_data):
        user = User.objects.create_superuser(
            validated_data['username'],
            validated_data['email'],
            validated_data['password'],
        )
        return user
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class KYCSerializer(serializers.ModelSerializer):
    class Meta:
        model = KYC
        fields = '__all__'

class CustomUserSerializer(serializers.ModelSerializer):
    kyc = KYCSerializer(many=True, read_only=True)
    cards = CardSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = '__all__'


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'
