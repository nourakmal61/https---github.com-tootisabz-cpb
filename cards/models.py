from django.db import models
from users.models import CustomUser
import random, string
from django.conf import settings



class Card(models.Model):
    BANK_CHOISE = (
        ('AZB', 'Azizi Bank'),
        ('NKB', 'New Kabul Bank'),
        ('MWB', 'Maiwand Bank'),
        ('maiwand_b', 'Maiwand Bank'),
        ('BMA', 'Bank Mili Afghan'),
        ('AUB', 'Afghan United Bank'),
        ('AIB', 'Afghanistan International Bank'),
    )
    id = models.AutoField(primary_key=True)
    bank_account = models.CharField(max_length=20, choices=BANK_CHOISE, default='disabled', blank=True)
    card_number = models.CharField(max_length=16, blank=True, unique=True)
    expiration_date = models.DateField()
    cvv = models.CharField(max_length=4, default=''.join(random.choices(string.digits, k=3)))
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.card_number
