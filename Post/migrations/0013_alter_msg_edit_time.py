# Generated by Django 3.2.9 on 2022-06-19 15:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Post', '0012_alter_msg_edit_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='msg',
            name='Edit_Time',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 19, 21, 0, 36, 993372)),
        ),
    ]
