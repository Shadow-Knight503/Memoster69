# Generated by Django 3.2.9 on 2022-05-27 05:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Post', '0002_alter_msg_edit_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='msg',
            name='Replied_Msg',
        ),
        migrations.AlterField(
            model_name='comment',
            name='cmnt_chn',
            field=models.CharField(default='1', max_length=100),
        ),
        migrations.AlterField(
            model_name='msg',
            name='Edit_Time',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 27, 10, 33, 54, 94803)),
        ),
        migrations.AlterField(
            model_name='msg',
            name='Reply',
            field=models.CharField(default='None', max_length=15),
        ),
    ]
