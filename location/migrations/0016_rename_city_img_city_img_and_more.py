# Generated by Django 5.0.6 on 2024-06-29 09:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0015_remove_project_facilities_alter_project_city_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='city',
            old_name='city_img',
            new_name='img',
        ),
        migrations.RenameField(
            model_name='country',
            old_name='country_img',
            new_name='img',
        ),
        migrations.RenameField(
            model_name='neighborhood',
            old_name='neighborhood_img',
            new_name='img',
        ),
        migrations.RenameField(
            model_name='projectbuildingplan',
            old_name='image',
            new_name='img',
        ),
        migrations.RenameField(
            model_name='projectimage',
            old_name='image',
            new_name='img',
        ),
        migrations.RenameField(
            model_name='propertybuildingplan',
            old_name='image',
            new_name='img',
        ),
        migrations.RenameField(
            model_name='propertyimage',
            old_name='image',
            new_name='img',
        ),
        migrations.RenameField(
            model_name='propertyoutwardview',
            old_name='image',
            new_name='img',
        ),
    ]
