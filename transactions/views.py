# transactions/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Transaction, Refund
from .serializers import TransactionSerializer, RefundSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def perform_create(self, serializer):
        transaction_type = serializer.validated_data['transaction_type']
        amount = serializer.validated_data['amount']
        account = serializer.validated_data['account']
        
        if transaction_type == 'transfer':
            to_user = serializer.validated_data['to_user']
            account.balance -= amount
            account.save()
            to_user.balance += amount
            to_user.save()
        
        elif transaction_type == 'deposit':
            account.balance += amount
            account.save()
        
        elif transaction_type == 'withdraw' or transaction_type == 'payment':
            account.balance -= amount
            account.save()
        
        serializer.save(balance_after_transaction=account.balance)
        

class RefundViewSet(viewsets.ModelViewSet):
    queryset = Refund.objects.all()
    serializer_class = RefundSerializer

    def perform_create(self, serializer): # type: ignore
        refund_amount = serializer.validated_data['refund_amount']
        transaction = serializer.validated_data['transaction']

        if not transaction.is_refunded:
            sender_account = transaction.account
            recipient_account = transaction.to_user if transaction.to_user else transaction.account
            
            # Calculate the refunded amount for each account
            if transaction.transaction_type == 'transfer':
                sender_refund_amount = refund_amount
                recipient_refund_amount = refund_amount
            else:
                sender_refund_amount = refund_amount
                recipient_refund_amount = 0
            
            # Check if recipient has sufficient balance for refund
            if recipient_account.balance >= recipient_refund_amount:
                # Adjust balances for refund
                sender_account.balance += sender_refund_amount
                recipient_account.balance -= recipient_refund_amount

                # Save the updated account balances
                sender_account.save()
                recipient_account.save()

                # Mark the transaction as refunded
                transaction.is_refunded = True
                transaction.save()

                # Display success message
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                # Display insufficient balance message
                return Response({'error': 'Insufficient balance in the receiver\'s account.'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save(is_processed=True)