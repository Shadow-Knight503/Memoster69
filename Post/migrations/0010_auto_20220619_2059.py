# Generated by Django 3.2.9 on 2022-06-19 15:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Post', '0009_auto_20220619_2058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='Points',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='meme',
            name='Points',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='msg',
            name='Edit_Time',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 19, 20, 59, 27, 287022)),
        ),
    ]
