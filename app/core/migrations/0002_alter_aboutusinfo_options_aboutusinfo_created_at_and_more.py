# Generated by Django 5.0.6 on 2024-07-10 14:13

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='aboutusinfo',
            options={'ordering': ['id']},
        ),
        migrations.AddField(
            model_name='aboutusinfo',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='aboutusinfo',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
