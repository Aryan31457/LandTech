# Generated by Django 4.2.16 on 2024-12-05 19:47

import cloudinary.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_floormap_prompt'),
    ]

    operations = [
        migrations.AlterField(
            model_name='floormap',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='floormap',
            name='floor_type',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='floormap',
            name='image',
            field=cloudinary.models.CloudinaryField(default=1, max_length=255, verbose_name='image'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='floormap',
            name='length',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='floormap',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='floormap',
            name='num_bathrooms',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='floormap',
            name='num_bedrooms',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='floormap',
            name='num_kitchens',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='floormap',
            name='num_rooms',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='floormap',
            name='num_washrooms',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='floormap',
            name='prompt',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='floormap',
            name='width',
            field=models.FloatField(),
        ),
    ]
