# Generated by Django 4.2.17 on 2025-01-06 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled'), ('completed', 'Completed'), ('no_show', 'No Show'), ('customer_confirmation_required', 'Customer Confirmation Required')], default='pending', max_length=30),
        ),
    ]
