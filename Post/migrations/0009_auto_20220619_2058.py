# Generated by Django 3.2.9 on 2022-06-19 15:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Post', '0008_alter_msg_edit_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='Points',
            field=models.IntegerField(default=0, max_length=10),
        ),
        migrations.AlterField(
            model_name='meme',
            name='Points',
            field=models.IntegerField(default=0, max_length=10),
        ),
        migrations.AlterField(
            model_name='msg',
            name='Edit_Time',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 19, 20, 58, 48, 750809)),
        ),
    ]