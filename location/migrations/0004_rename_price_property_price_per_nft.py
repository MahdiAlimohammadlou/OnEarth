# Generated by Django 5.0.6 on 2024-05-23 06:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0003_property_floor_property_heating_option_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='property',
            old_name='price',
            new_name='price_per_nft',
        ),
    ]
