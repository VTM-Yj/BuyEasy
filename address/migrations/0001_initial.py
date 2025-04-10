# Generated by Django 5.1.7 on 2025-03-15 22:42

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.PositiveIntegerField()),
                ('address_line1', models.CharField(help_text='Street address and number', max_length=100)),
                ('address_line2', models.CharField(blank=True, help_text='Apartment or unit (optional)', max_length=100, null=True)),
                ('city', models.CharField(help_text='City', max_length=50)),
                ('county', models.CharField(help_text='County or region', max_length=50)),
                ('postcode', models.CharField(help_text='Postcode', max_length=10, validators=[django.core.validators.RegexValidator(message="Please enter a valid UK postcode, e.g. 'SW1A 1AA'.", regex='^[A-Z]{1,2}\\d[A-Z\\d]?\\s*\\d[A-Z]{2}$')])),
                ('phone', models.CharField(blank=True, help_text='Phone number (optional)', max_length=20, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
