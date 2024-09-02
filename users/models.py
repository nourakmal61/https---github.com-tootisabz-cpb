from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from django.conf import settings
import random
import string
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

PREFIX = 'CP'

def generate_unique_account_number():
    prefix = settings.ACCOUNT_NUMBER_PREFIX
    unique_suffix = ''.join(random.choices(string.digits, k=6))
    return f"{prefix}-{unique_suffix}"

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, password, **extra_fields)

class CustomUser(AbstractBaseUser):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('disabled', 'Disabled'),
    ]
    ACCOUNT_CHOICES = (
        ('personal', 'Personal'),
        ('business', 'Business'),
    )
    CURRENCY_CHOICES = (
        ('USD', 'USD'),
        ('AFN', 'AFN'),
    )
    id = models.AutoField(primary_key=True,  unique=True)
    email = models.EmailField(max_length=254, unique=True)
    phone_number = models.CharField(max_length=15, default='0000000000')
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    date_of_birth = models.DateField(null=True, blank=True)
    last_login = models.DateTimeField(null=True, blank=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    user_status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='disabled')
    address = models.CharField(max_length=255)
    account_number = models.CharField(max_length=20, blank=True, unique=True)
    account_type = models.CharField(max_length=10, choices=ACCOUNT_CHOICES)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0) # type: ignore 
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Relationship to BeneficiaryAccount from the new beneficiaries app
    # beneficiary_accounts = models.ManyToManyField('beneficiaries.BeneficiaryAccount', null=True, blank=True, default='disabled', related_name='new_beneficiaries_account')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        abstract = False

    def save(self, *args, **kwargs):
        if not self.account_number or not self.account_number.startswith(settings.ACCOUNT_NUMBER_PREFIX):
            self.account_number = generate_unique_account_number()
        super().save(*args, **kwargs)


class KYC(models.Model):
    KYC_TYPE_CHOICES = [
        ('passport', 'Passport'),
        ('nid', 'National ID'),
        ('business_license', 'Business License')
    ]

    id = models.AutoField(primary_key=True)
    userid = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='kyc')
    kyc_type = models.CharField(max_length=30, choices=KYC_TYPE_CHOICES)
    kyc_media_front = models.ImageField(upload_to='kyc_front/')
    kyc_media_back = models.ImageField(upload_to='kyc_back/', blank=True, null=True)
    selfie = models.ImageField(upload_to='selfies/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'KYC'
        verbose_name_plural = 'KYC Documents'


class Wallet(models.Model):
    id = models.AutoField(primary_key=True)
    userid = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

@receiver(pre_save, sender=Wallet)
def get_previous_balance(sender, instance, **kwargs):
    from .models import Wallet  # Import Wallet model here
    if instance.pk:
        try:
            old_instance = Wallet.objects.get(pk=instance.pk)
            instance.previous_balance = old_instance.wallet_balance
        except Wallet.DoesNotExist:
            pass

@receiver(post_save, sender=Wallet)
def update_user_balance(sender, instance, created, **kwargs):
    from .models import Wallet  # Import Wallet model here
    user = instance.userid
    if created:
        user.balance += instance.wallet_balance
    else:
        user.balance = user.balance - instance.previous_balance + instance.wallet_balance
    user.save()

@receiver(pre_delete, sender=Wallet)
def adjust_user_balance(sender, instance, **kwargs):
    from .models import Wallet  # Import Wallet model here
    user = instance.userid
    user.balance -= instance.wallet_balance
    user.save()


    

