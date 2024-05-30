# Generated by Django 5.0.6 on 2024-05-20 13:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('phone_number', models.CharField(blank=True, max_length=11, null=True, unique=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_seller', models.BooleanField(default=False)),
                ('is_buyer', models.BooleanField(default=False)),
                ('is_agent', models.BooleanField(default=False)),
                ('is_guest', models.BooleanField(default=True)),
                ('is_active', models.BooleanField(default=False)),
                ('otp_code', models.CharField(blank=True, max_length=6, null=True)),
                ('otp_created_at', models.DateTimeField(blank=True, null=True)),
                ('is_phone_verified', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AgentInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=255)),
                ('company_address', models.CharField(max_length=255)),
                ('company_email', models.EmailField(max_length=255)),
                ('company_phone_number', models.CharField(max_length=11)),
                ('biometric', models.ImageField(upload_to='biometric_images/')),
                ('business_card', models.ImageField(upload_to='business_card_images/')),
                ('id_card', models.ImageField(upload_to='id_card_images/')),
                ('agent_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='agent_info', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BuyerPersonalInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('biometric', models.ImageField(upload_to='biometric_images/')),
                ('full_name', models.CharField(max_length=100)),
                ('postal_address', models.TextField()),
                ('marital_status', models.CharField(choices=[('single', 'Single'), ('married', 'Married')], max_length=20)),
                ('marriage_contract', models.ImageField(blank=True, null=True, upload_to='marriage_contract_images/')),
                ('elec_bill', models.ImageField(upload_to='elec_bill_images/')),
                ('birth_certificate', models.ImageField(upload_to='birth_certificate_images/')),
                ('id_or_driver_license', models.ImageField(upload_to='id_or_driver_license_images/')),
                ('buyer_agreement', models.ImageField(upload_to='buyer_aggrement_images/')),
                ('buyer_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='buyer_personal_info', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SellerPersonalInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('biometric', models.ImageField(upload_to='biometric_images/')),
                ('full_name', models.CharField(max_length=100)),
                ('postal_address', models.TextField()),
                ('marital_status', models.CharField(choices=[('single', 'Single'), ('married', 'Married')], max_length=20)),
                ('marriage_contract', models.ImageField(blank=True, null=True, upload_to='marriage_contract_images/')),
                ('elec_bill', models.ImageField(upload_to='elec_bill_images/')),
                ('birth_certificate', models.ImageField(upload_to='birth_certificate_images/')),
                ('id_or_driver_license', models.ImageField(upload_to='id_or_driver_license_images/')),
                ('passport', models.ImageField(upload_to='passport_images/')),
                ('seller_agreement', models.ImageField(upload_to='seller_aggrement_images/')),
                ('seller_user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='seller_personal_info', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
