# Generated by Django 5.0.7 on 2024-08-29 04:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(default='0000000000', max_length=15)),
                ('username', models.CharField(max_length=150, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=6)),
                ('user_status', models.CharField(choices=[('active', 'Active'), ('disabled', 'Disabled')], default='disabled', max_length=8)),
                ('address', models.CharField(max_length=255)),
                ('account_number', models.CharField(blank=True, max_length=20, unique=True)),
                ('account_type', models.CharField(choices=[('personal', 'Personal'), ('business', 'Business')], max_length=10)),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('currency', models.CharField(choices=[('USD', 'USD'), ('AFN', 'AFN')], max_length=3)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='KYC',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('kyc_type', models.CharField(choices=[('passport', 'Passport'), ('nid', 'National ID'), ('business_license', 'Business License')], max_length=30)),
                ('kyc_media_front', models.ImageField(upload_to='kyc_front/')),
                ('kyc_media_back', models.ImageField(blank=True, null=True, upload_to='kyc_back/')),
                ('selfie', models.ImageField(upload_to='selfies/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kyc', to='users.customuser')),
            ],
            options={
                'verbose_name': 'KYC',
                'verbose_name_plural': 'KYC Documents',
            },
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('wallet_balance', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.customuser')),
            ],
        ),
    ]
