from rest_framework import serializers
from .models import BeneficiaryAccount

class BeneficiaryAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BeneficiaryAccount
        fields = ['id', 'userid', 'full_name', 'phone_number', 'address', 'account_number', 'created_at', 'updated_at']