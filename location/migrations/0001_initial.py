# Generated by Django 5.0.6 on 2024-05-20 13:17

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.TextField()),
                ('banner_img', models.ImageField(blank=True, null=True, upload_to='banner_images/')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=100)),
                ('category_icon', models.ImageField(blank=True, null=True, upload_to='category_images/')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=3, unique=True)),
                ('flag_img', models.ImageField(blank=True, null=True, upload_to='country_flags/')),
                ('country_img', models.ImageField(blank=True, null=True, upload_to='country_images/')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('facility_icon', models.ImageField(blank=True, null=True, upload_to='facility_icons/')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('average_groth', models.DecimalField(decimal_places=2, max_digits=6)),
                ('city_img', models.ImageField(blank=True, null=True, upload_to='city_images/')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='location.country')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('average_rating', models.DecimalField(decimal_places=1, default=5.0, max_digits=2, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('address', models.CharField(max_length=255)),
                ('cover_img', models.ImageField(blank=True, null=True, upload_to='project_cover_images/')),
                ('slug', models.SlugField(blank=True, max_length=150, unique=True)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='location.city')),
                ('facilities', models.ManyToManyField(to='location.facility')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProjectImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='project_images/')),
                ('image_2d', models.ImageField(blank=True, null=True, upload_to='project_images_2d/')),
                ('image_3d', models.ImageField(blank=True, null=True, upload_to='project_images_3d/')),
                ('project', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='image', to='location.project')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('location', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('area', models.DecimalField(decimal_places=2, max_digits=10)),
                ('bedrooms', models.IntegerField()),
                ('bathrooms', models.IntegerField()),
                ('purpose', models.CharField(max_length=255)),
                ('furnished', models.BooleanField()),
                ('parking_space_count', models.IntegerField()),
                ('has_maid_room', models.BooleanField()),
                ('has_swimming_pool', models.BooleanField()),
                ('has_steam_room', models.BooleanField()),
                ('average_rating', models.DecimalField(decimal_places=1, default=5.0, max_digits=2, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('cover_img', models.ImageField(blank=True, null=True, upload_to='property_cover_images/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='location.category')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='properties', to='location.project')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PropertyImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='Property_images/')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='location.property')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
