# Generated by Django 5.0.7 on 2024-09-02 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0004_alter_card_cvv'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='cvv',
            field=models.CharField(default='279', max_length=4),
        ),
    ]
