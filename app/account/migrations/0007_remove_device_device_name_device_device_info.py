# Generated by Django 5.0.6 on 2024-06-06 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_remove_device_access_token_remove_device_created_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='device_name',
        ),
        migrations.AddField(
            model_name='device',
            name='device_info',
            field=models.CharField(default='Unknown Device', max_length=255),
        ),
    ]
