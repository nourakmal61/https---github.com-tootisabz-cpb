from django.db import models
from django.conf import settings
from users.models import CustomUser
import random
import string

PREFIX = 'CP'

def generate_unique_account_number():
    prefix = settings.ACCOUNT_NUMBER_PREFIX
    unique_suffix = ''.join(random.choices(string.digits, k=6))
    return f"{prefix}-{unique_suffix}"

class BeneficiaryAccount(models.Model):
    id = models.AutoField(primary_key=True)
    userid = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='beneficiaries')
    full_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15, default='0000000000')
    email = models.EmailField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True)
    account_number = models.CharField(max_length=20, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.account_number or not self.account_number.startswith(settings.ACCOUNT_NUMBER_PREFIX):
            self.account_number = generate_unique_account_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} - {self.account_number}"