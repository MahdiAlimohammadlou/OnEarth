# Generated by Django 5.0.6 on 2024-07-15 18:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('financial', '0003_alter_nft_options_alter_shippinginfo_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shippinginfo',
            name='payoff_price',
        ),
    ]
