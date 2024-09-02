from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['account', 'amount', 'balance_after_transaction', 'transaction_type', 'timestamp']
    list_filter = ['transaction_type', 'timestamp']
    search_fields = ['account__account_number', 'amount']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('account')

    def transfer_transactions(self, request, queryset):
        queryset.update(transaction_type='transfer')
    transfer_transactions.short_description = 'Mark selected transactions as Transfer' # type: ignore

    def deposit_transactions(self, request, queryset):
        queryset.update(transaction_type='deposit')
    deposit_transactions.short_description = 'Mark selected transactions as Deposit' # type: ignore

    def withdraw_transactions(self, request, queryset):
        queryset.update(transaction_type='withdraw')
    withdraw_transactions.short_description = 'Mark selected transactions as Withdraw' # type: ignore

    def payment_transactions(self, request, queryset):
        queryset.update(transaction_type='payment')
    payment_transactions.short_description = 'Mark selected transactions as Payment' # type: ignore

    def interest_transactions(self, request, queryset):
        queryset.update(transaction_type='interest')
    interest_transactions.short_description = 'Mark selected transactions as Interest' # type: ignore

    def fee_transactions(self, request, queryset):
        queryset.update(transaction_type='fee')
    fee_transactions.short_description = 'Mark selected transactions as Fee' # type: ignore

    actions = [transfer_transactions, deposit_transactions, withdraw_transactions, payment_transactions, interest_transactions, fee_transactions] # type: ignore adsfadsfasfa
