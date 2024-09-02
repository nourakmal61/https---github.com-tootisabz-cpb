from django.db import models
from users.models import CustomUser

class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = (
        ('transfer', 'Transfer'),
        ('deposit', 'Deposit'),
        ('withdraw', 'Withdraw'),
        ('payment', 'Payment'),
    )
    id = models.AutoField(primary_key=True)
    account = models.ForeignKey(CustomUser, related_name='transactions', on_delete=models.CASCADE)
    to_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_transactions', blank=True, null=True)
    amount = models.DecimalField(decimal_places=2, max_digits=12)
    balance_after_transaction = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    transaction_type = models.CharField(choices=TRANSACTION_TYPE_CHOICES, max_length=10)
    is_refunded = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.account.account_number)

    class Meta:
        ordering = ['timestamp']

class Refund(models.Model):
    id = models.AutoField(primary_key=True)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    refund_amount = models.DecimalField(decimal_places=2, max_digits=12)
    is_processed = models.BooleanField(default=False)

    def __str__(self):
        return f"Refund for Transaction ID: {self.transaction.id}"