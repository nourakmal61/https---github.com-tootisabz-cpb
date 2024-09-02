# Generated by Django 5.0.7 on 2024-08-29 04:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('bank_account', models.CharField(blank=True, choices=[('AZB', 'Azizi Bank'), ('NKB', 'New Kabul Bank'), ('MWB', 'Maiwand Bank'), ('maiwand_b', 'Maiwand Bank'), ('BMA', 'Bank Mili Afghan'), ('AUB', 'Afghan United Bank'), ('AIB', 'Afghanistan International Bank')], default='disabled', max_length=20)),
                ('card_number', models.CharField(blank=True, max_length=16, unique=True)),
                ('expiration_date', models.DateField()),
                ('cvv', models.CharField(default='014', max_length=4)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.customuser')),
            ],
        ),
    ]
