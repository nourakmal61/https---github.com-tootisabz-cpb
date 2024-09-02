from django.contrib import admin
from .models import BeneficiaryAccount

@admin.register(BeneficiaryAccount)
class BeneficiaryAccountAdmin(admin.ModelAdmin):
    list_display = ['id', 'userid', 'full_name', 'phone_number', 'address', 'account_number', 'created_at', 'updated_at']
    list_filter = ['userid']
    search_fields = ['full_name', 'account_number']