# Generated by Django 4.2.16 on 2024-12-05 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_floormap_num_bathrooms_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='floormap',
            name='length',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='floormap',
            name='width',
            field=models.PositiveIntegerField(default=1),
        ),
    ]