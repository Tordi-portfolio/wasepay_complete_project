from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm
from django.contrib import messages
from .models import Wallet, Plan, WithdrawalRequest, PasswordReset
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.utils import timezone
from django.core.mail import EmailMessage
from django.urls import reverse
from django.shortcuts import render
from django.db.models import F
from decimal import Decimal


def chart(request):
    return render(request, 'chart.html')

def wallet(request):
    return render(request, 'wallet.html')

def invest_guide(request):
    return render(request, 'invest_guide.html')

def about(request):
    return render(request, 'about.html')

def rules(request):
    return render(request, 'rules.html')

def services(request):
    return render(request, 'services.html')


@login_required
def selectpay(request):
    return render(request, 'payment/selectpay.html', {})

@login_required
def eth(request):
    return render(request, 'payment/eth.html', {})

@login_required
def usdt(request):
    return render(request, 'payment/usdt.html', {})

@login_required
def solana(request):
    return render(request, 'payment/solana.html', {})

@login_required
def ton(request):
    return render(request, 'payment/ton.html', {})

@login_required
def withdraw(request):
    if request.method == 'POST':
        crypto_type = request.POST.get('crypto_type')
        try:
            amount = Decimal(request.POST.get('amount'))
        except:
            messages.error(request, "Invalid amount entered.")
            return redirect('withdraw')

        wallet_address = request.POST.get('wallet_address')
        password = request.POST.get('password')
        user = request.user

        # Password check
        if not authenticate(username=user.username, password=password):
            messages.error(request, "Incorrect password.")
            return redirect('withdraw')

        wallet = Wallet.objects.get(user=user)

        # Minimum withdrawal amounts
        min_withdrawals = {
            'usdt': Decimal('200'),
            'eth': Decimal('1'),
            'solana': Decimal('2'),
            'ton': Decimal('20')
        }

        # Balance mapping
        balances = {
            'usdt': wallet.balance,
            'eth': wallet.eth,
            'solana': wallet.solana,
            'ton': wallet.ton
        }

        if crypto_type not in balances:
            messages.error(request, "Invalid cryptocurrency selected.")
            return redirect('withdraw')

        if amount < min_withdrawals[crypto_type]:
            messages.error(request, f"Minimum withdrawal for {crypto_type.upper()} is {min_withdrawals[crypto_type]}")
            return redirect('withdraw')

        if amount > balances[crypto_type]:
            messages.error(request, f"Insufficient {crypto_type.upper()} balance.")
            return redirect('withdraw')

        # Deduct the amount
        if crypto_type == 'usdt':
            wallet.balance -= amount
        elif crypto_type == 'eth':
            wallet.eth -= amount
        elif crypto_type == 'solana':
            wallet.solana -= amount
        elif crypto_type == 'ton':
            wallet.ton -= amount
        wallet.save()

        # Create withdrawal request
        WithdrawalRequest.objects.create(
            user=user,
            crypto_type=crypto_type,
            amount=amount,
            wallet_address=wallet_address,
            status='pending'
        )

        messages.success(request, "Withdrawal request submitted successfully.")
        return redirect('dashboard')

    return render(request, 'withdraw.html')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Account created successfully!")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Successfully Login...")
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, "Successfully Logout...")
    return redirect('home')


def home(request):
    return render(request, 'home.html', {})

def base(request):
    return render(request, 'base.html', {})

def dashboard(request):
    posts = Plan.objects.all()
    wallet, created = Wallet.objects.get_or_create(user=request.user)
    return render(request, 'plan/dashboard.html', {'wallet': wallet, 'posts': posts})


def view_plan(request, pk):
    posts = Plan.objects.get(id=pk)
    return render(request, 'plan/view_plan.html', {'posts': posts})

def ForgotPassword(request):
    if request.method == "POST":
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)

            new_password_reset = PasswordReset(user=user)
            new_password_reset.save()

            password_reset_url = reverse('reset-password', kwargs={'reset_id': new_password_reset.reset_id})

            full_password_reset_url = f'{request.scheme}://{request.get_host()}{password_reset_url}'

            email_body = f'Reset your password using the link below:\n\n\n{full_password_reset_url}'
        
            email_message = EmailMessage(
                'Reset your password', # email subject
                email_body,
                settings.EMAIL_HOST_USER, # email sender
                [email] # email  receiver 
            )

            email_message.fail_silently = True
            email_message.send()
            return redirect('password-reset-sent', reset_id=new_password_reset.reset_id)

        except User.DoesNotExist:
            messages.error(request, f"No user with email '{email}' found")
            return redirect('forgot-password')
    return render(request, 'accounts/forgot_password.html')


def PasswordResetSent(request, reset_id):

    if PasswordReset.objects.filter(reset_id=reset_id).exists():
        return render(request, 'accounts/password_reset_sent.html')
    else:
        # redirect to forgot password page if code does not exist
        messages.error(request, 'Invalid reset id')

    return redirect('forgot_password')



def ResetPassword(request, reset_id):

    try:
        password_reset_id = PasswordReset.objects.get(reset_id=reset_id)

        if request.method == "POST":
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            passwords_have_error = False

            if password != confirm_password:
                passwords_have_error = True
                messages.error(request, 'Passwords do not match')

            if len(password) < 5:
                passwords_have_error = True
                messages.error(request, 'Password must be at least 5 characters long')

            expiration_time = password_reset_id.created_when + timezone.timedelta(minutes=10)

            if timezone.now() > expiration_time:
                passwords_have_error = True
                messages.error(request, 'Reset link has expired')

                password_reset_id.delete()

            if not passwords_have_error:
                user = password_reset_id.user
                user.set_password(password)
                user.save()

                password_reset_id.delete()

                messages.success(request, 'Password reset. Proceed to login')
                return redirect('login')
            else:
                # redirect back to password reset page and display errors
                return redirect('reset-password', reset_id=reset_id)

    
    except PasswordReset.DoesNotExist:
        
        # redirect to forgot password page if code does not exist
        messages.error(request, 'Invalid reset id')
        return redirect('forgot-password')
        
    return render(request, 'accounts/reset_password.html')



# app/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from .forms import TransactionForm
from .models import Transaction

def superuser_only(view_func):
    return user_passes_test(lambda u: u.is_superuser)(view_func)

@superuser_only
def create_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transaction_list')  # or success message
    else:
        form = TransactionForm()
    return render(request, 'create_transaction.html', {'form': form})


# views.py
from django.contrib.admin.views.decorators import staff_member_required
from .models import Transaction

@staff_member_required
def transaction_list(request):
    transactions = Transaction.objects.all().order_by('-created_at')
    return render(request, 'transaction_list.html', {'transactions': transactions})


# app/views.py
from django.contrib.auth.decorators import login_required

@login_required
def my_transactions(request):
    user = request.user
    transactions = user.transactions.all().order_by('-created_at')  # using related_name
    return render(request, 'my_transactions.html', {'transactions': transactions})


import requests
from bs4 import BeautifulSoup
from .scraper import scrape_crypto_table

# Create your views here.

def price(request):
    data = scrape_crypto_table()
    query = request.GET.get('q', '').lower()

    if query:
        data = [
            coin for coin in data
            if query in coin['name'].lower() or query in coin['code'].lower()
        ]

    return render(request, 'price.html', {'data': data, 'query': query})


def wallet(request):
    posts = Plan.objects.all()
    wallet, created = Wallet.objects.get_or_create(user=request.user)
    return render(request, 'wallet.html', {'wallet': wallet, 'posts': posts})
