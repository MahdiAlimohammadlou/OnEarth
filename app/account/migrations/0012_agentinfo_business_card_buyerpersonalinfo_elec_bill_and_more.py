# Generated by Django 5.0.6 on 2024-07-06 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_remove_agentinfo_basic_approval_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='agentinfo',
            name='business_card',
            field=models.ImageField(blank=True, null=True, upload_to='business_card_images/'),
        ),
        migrations.AddField(
            model_name='buyerpersonalinfo',
            name='elec_bill',
            field=models.ImageField(blank=True, null=True, upload_to='elec_bill_images/'),
        ),
        migrations.AddField(
            model_name='sellerpersonalinfo',
            name='elec_bill',
            field=models.ImageField(blank=True, null=True, upload_to='elec_bill_images/'),
        ),
    ]
