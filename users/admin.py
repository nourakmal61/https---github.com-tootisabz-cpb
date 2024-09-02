from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, KYC, Wallet

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['id', 'email', 'username', 'first_name', 'last_name', 'is_superuser', 'is_staff', 'is_active']
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'date_of_birth', 'gender', 'address')}),
        ('Account Info', {'fields': ('account_number', 'account_type', 'currency', 'user_status')}),
        ('Permissions', {'fields': ('is_superuser', 'is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )
    search_fields = ['email', 'username', 'first_name', 'last_name']
    ordering = ['email']
    filter_horizontal = ()
    list_filter = ['is_superuser', 'is_staff', 'is_active']
    exclude = ['date_joined']

admin.site.register(CustomUser, CustomUserAdmin)

class KYCAdmin(admin.ModelAdmin):
    list_display = ['userid', 'kyc_type', 'created_at', 'updated_at']
    list_filter = ['kyc_type']
    search_fields = ['userid__email']

admin.site.register(KYC, KYCAdmin)


class WalletAdmin(admin.ModelAdmin):
    list_display = ['id', 'userid', 'wallet_balance', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['userid__email']

admin.site.register(Wallet, WalletAdmin)
