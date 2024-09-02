from django.contrib import admin
from .models import Card

@admin.register(Card)
class TransferAdmin(admin.ModelAdmin):
    list_display = ['id', 'bank_account', 'card_number', 'expiration_date', 'cvv','owner','is_active']
