# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Wallet

@receiver(post_save, sender=User)
def create_user_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance)



# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import WithdrawalRequest, Transaction

@receiver(post_save, sender=WithdrawalRequest)
def create_transaction_for_withdrawal(sender, instance, created, **kwargs):
    if created:
        Transaction.objects.create(
            user=instance.user,
            transaction_type='withdrawal',
            amount=instance.amount,
            status='pending',
            wallet_address=instance.wallet_address
        )
