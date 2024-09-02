from rest_framework import viewsets
from .models import BeneficiaryAccount
from .serializers import BeneficiaryAccountSerializer

class BeneficiaryAccountViewSet(viewsets.ModelViewSet):
    queryset = BeneficiaryAccount.objects.all()
    serializer_class = BeneficiaryAccountSerializer