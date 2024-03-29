# Generated by Django 3.2.9 on 2022-03-14 12:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Register_Page', '0003_alter_userprofile_profile_pic'),
    ]

    operations = [
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nav_Back', models.CharField(default='#020440', max_length=7)),
                ('Nav_Color', models.CharField(default='#d8c70e', max_length=7)),
                ('Nav_Line', models.CharField(default='#d8c70e', max_length=7)),
                ('Body_Back', models.CharField(default='#2d2424', max_length=7)),
                ('Card_Back', models.CharField(default='#2d2424', max_length=7)),
                ('Card_Color', models.CharField(default='#ffffff', max_length=7)),
                ('Card_Border', models.CharField(default='#020440', max_length=7)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Register_Page.userprofile')),
            ],
        ),
    ]
