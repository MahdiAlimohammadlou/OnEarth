# Generated by Django 5.0.6 on 2024-07-11 21:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0026_alter_projectfacilities_project_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectdetails',
            name='levels',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='projectdetails',
            name='plot_area',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='projectdetails',
            name='total_construction_area',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='projectdetails',
            name='total_height',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='projectdetails',
            name='type',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='projectfacilities',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projectfacilities', to='location.project'),
        ),
    ]
