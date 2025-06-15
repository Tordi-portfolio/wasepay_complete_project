from django.contrib import admin
from .models import Plan, Wallet, WithdrawalRequest, Transaction
# Register your models here.

admin.site.register(Plan)
admin.site.register(Wallet)
admin.site.register(Transaction)
admin.site.register(WithdrawalRequest)