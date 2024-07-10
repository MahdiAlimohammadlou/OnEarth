# Generated by Django 5.0.6 on 2024-07-10 14:13

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0022_project_apartment_type_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='property',
            name='category',
        ),
        migrations.AlterModelOptions(
            name='banner',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='city',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='country',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='locationfeature',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='neighborhood',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='projectbuildingplan',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='projectimage',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='projectvideo',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='property',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='propertybuildingplan',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='propertyimage',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='propertyoutwardview',
            options={'ordering': ['id']},
        ),
        migrations.AlterModelOptions(
            name='propertyvideo',
            options={'ordering': ['id']},
        ),
        migrations.RenameField(
            model_name='property',
            old_name='floor',
            new_name='balcony_count',
        ),
        migrations.RenameField(
            model_name='property',
            old_name='unit_number',
            new_name='closet_count',
        ),
        migrations.RenameField(
            model_name='property',
            old_name='has_balcony',
            new_name='is_open_kichen',
        ),
        migrations.RemoveField(
            model_name='project',
            name='apartment_type_count',
        ),
        migrations.RemoveField(
            model_name='project',
            name='floor_count',
        ),
        migrations.RemoveField(
            model_name='project',
            name='has_gym',
        ),
        migrations.RemoveField(
            model_name='project',
            name='has_meeting_room',
        ),
        migrations.RemoveField(
            model_name='project',
            name='has_music_room',
        ),
        migrations.RemoveField(
            model_name='project',
            name='has_parking',
        ),
        migrations.RemoveField(
            model_name='project',
            name='has_party_room',
        ),
        migrations.RemoveField(
            model_name='project',
            name='has_pool',
        ),
        migrations.RemoveField(
            model_name='project',
            name='has_security',
        ),
        migrations.RemoveField(
            model_name='project',
            name='has_spa',
        ),
        migrations.RemoveField(
            model_name='project',
            name='has_theater',
        ),
        migrations.RemoveField(
            model_name='project',
            name='has_yoga_room',
        ),
        migrations.RemoveField(
            model_name='project',
            name='roofed_parking',
        ),
        migrations.RemoveField(
            model_name='project',
            name='roofed_pool',
        ),
        migrations.RemoveField(
            model_name='projectvideo',
            name='description',
        ),
        migrations.RemoveField(
            model_name='projectvideo',
            name='title',
        ),
        migrations.RemoveField(
            model_name='property',
            name='description',
        ),
        migrations.RemoveField(
            model_name='property',
            name='has_bathroom',
        ),
        migrations.RemoveField(
            model_name='property',
            name='has_bedroom',
        ),
        migrations.RemoveField(
            model_name='property',
            name='has_dining_room',
        ),
        migrations.RemoveField(
            model_name='property',
            name='has_kitchen',
        ),
        migrations.RemoveField(
            model_name='property',
            name='has_living_room',
        ),
        migrations.RemoveField(
            model_name='property',
            name='has_maid_room',
        ),
        migrations.RemoveField(
            model_name='property',
            name='has_steam_room',
        ),
        migrations.RemoveField(
            model_name='property',
            name='has_swimming_pool',
        ),
        migrations.RemoveField(
            model_name='property',
            name='name',
        ),
        migrations.RemoveField(
            model_name='property',
            name='purpose',
        ),
        migrations.RemoveField(
            model_name='propertyvideo',
            name='description',
        ),
        migrations.RemoveField(
            model_name='propertyvideo',
            name='title',
        ),
        migrations.AddField(
            model_name='locationfeature',
            name='type',
            field=models.CharField(blank=True, choices=[('Walk', 'walk'), ('Car', 'car')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='neighborhood',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='neighborhood',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='project',
            name='brochure',
            field=models.FileField(blank=True, null=True, upload_to='brochure_pdf/'),
        ),
        migrations.AddField(
            model_name='project',
            name='gym_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='project',
            name='kids_swimming_pool_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='project',
            name='landscaped_gardens_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='project',
            name='large_lifts',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='project',
            name='meeting_room_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='project',
            name='music_room_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='project',
            name='parking_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='project',
            name='party_room_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='project',
            name='pool_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='project',
            name='retail_areas_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='project',
            name='roofed_parking_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='project',
            name='roofed_pool_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='project',
            name='security_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='project',
            name='spa_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='project',
            name='theater_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='project',
            name='yoga_room_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='projectvideo',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='projectvideo',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='property',
            name='first_floor',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
        migrations.AddField(
            model_name='property',
            name='first_unit_number',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
        migrations.AddField(
            model_name='property',
            name='last_floor',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
        migrations.AddField(
            model_name='property',
            name='last_unit_number',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
        migrations.AddField(
            model_name='property',
            name='lundry_count',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
        migrations.AddField(
            model_name='propertylike',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='propertyvideo',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='propertyvideo',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='locationfeature',
            name='feature_time_in_minutes',
            field=models.IntegerField(blank=True, default=5, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='master_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='property',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='properties', to='location.project'),
        ),
        migrations.CreateModel(
            name='ProjectDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('type', models.CharField(max_length=255)),
                ('plot_area', models.CharField(max_length=255)),
                ('total_height', models.CharField(max_length=255)),
                ('total_construction_area', models.CharField(max_length=255)),
                ('levels', models.CharField(max_length=255)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='location.project')),
            ],
            options={
                'ordering': ['id'],
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='PropertyCategory',
        ),
    ]
