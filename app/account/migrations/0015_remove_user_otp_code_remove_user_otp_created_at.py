# Generated by Django 5.0.6 on 2024-07-24 12:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_buyerpersonalinfo_background_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='otp_code',
        ),
        migrations.RemoveField(
            model_name='user',
            name='otp_created_at',
        ),
    ]
