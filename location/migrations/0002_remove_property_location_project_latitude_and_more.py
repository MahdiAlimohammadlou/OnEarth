# Generated by Django 5.0.6 on 2024-05-21 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='property',
            name='location',
        ),
        migrations.AddField(
            model_name='project',
            name='latitude',
            field=models.FloatField(default=2214546),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='longitude',
            field=models.FloatField(default=6464),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='property',
            name='latitude',
            field=models.FloatField(default=65464),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='property',
            name='longitude',
            field=models.FloatField(default=6544),
            preserve_default=False,
        ),
    ]
