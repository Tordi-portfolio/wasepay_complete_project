from django.urls import path
from . import views
from .views import create_transaction, transaction_list, my_transactions

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('base', views.base, name='base'),
    path('withdraw', views.withdraw, name='withdraw'),
    path('create_transaction/', create_transaction, name='create_transaction'),
    path('transactions_list', transaction_list, name='transaction_list'),
    path('my_transactions/', my_transactions, name='my_transactions'),
    path('eth', views.eth, name='eth'),
    path('wallet', views.wallet, name='wallet'),

    path('selectpay', views.selectpay, name='selectpay'),
    path('eth', views.eth, name='eth'),
    path('usdt', views.usdt, name='usdt'),
    path('solana', views.solana, name='solana'),
    path('ton', views.ton, name='ton'),
    path('invest_guide', views.invest_guide, name='invest_guide'),
    path('chart', views.chart, name='chart'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('view_plan/<str:pk>', views.view_plan, name='view_plan'),

    path('forgot-password/', views.ForgotPassword, name='forgot-password'),
    path('password-reset-sent/<str:reset_id>/', views.PasswordResetSent, name='password-reset-sent'),
    path('reset-password/<str:reset_id>/', views.ResetPassword, name='reset-password'),

    path('rules', views.rules, name='rules'),
    path('services', views.services, name='services'),

    path('about', views.about, name='about'),
    path('price', views.price, name='price'),
]