from django.contrib.auth.models import User
from django.db import models
from cloudinary.models import CloudinaryField as BaseCloudinaryField
from django.conf import settings
from Register_Page.models import UserProfile
from datetime import datetime


# Create your models here.
class CloudinaryField(BaseCloudinaryField):
    def upload_options(self, model_instance):
        return {
            'public_id': model_instance.name,
            'filename': Meme.Title,
            'unique_filename': False,
            'overwrite': False,
            'resource_type': 'auto',
            'tags': ['Post'],
            'invalidate': True,
            'quality': 'auto:eco',
        }


class Meme(models.Model):
    Title = models.CharField(max_length=500)
    date_created = models.DateTimeField(auto_now_add=True)
    op = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    Post = CloudinaryField('Post', resource_type="auto")
    Type = models.CharField(max_length=50, default="Img")
    Points = models.IntegerField(default=5)
    Pinned = models.CharField(default=0, max_length=1)
    Daily = models.CharField(default=0, max_length=1)
    Day = models.CharField(default="None", max_length=50)
    Date = models.CharField(default="None", max_length=50)

    def __str__(self):
        return self.Title


class DayDecor(models.Model):
    Day = models.CharField(default="None", max_length=50)
    Logo = models.CharField(default="None", max_length=150)
    NavBack = models.CharField(default="None", max_length=50)
    NavColor = models.CharField(default="None", max_length=50)

    def __str__(self):
        return self.Day


class Saw(models.Model):
    Meme = models.ForeignKey(Meme, on_delete=models.CASCADE)
    Op = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    Seen = models.CharField(default='0', max_length=1)


class Comment(models.Model):
    not_post_method_ok = models.ForeignKey(Meme, on_delete=models.CASCADE, default=1)
    op = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    Points = models.IntegerField(default=1)
    comment = models.TextField(max_length=500)
    reply = models.CharField(default='0', max_length=1)
    cmnt_chn = models.CharField(default='1', max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.not_post_method_ok.Title}-{self.op}=>{self.comment}'


class Cmnt_Vote(models.Model):
    op = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    Cmnt = models.ForeignKey(Comment, on_delete=models.CASCADE, default=1, unique=False)
    voted = models.CharField(default='0', max_length=1)

    def __str__(self):
        return f'{self.Cmnt.comment}-{self.op}'


class Vote(models.Model):
    op = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    meme = models.ForeignKey(Meme, on_delete=models.CASCADE, default=1, unique=False)
    voted = models.CharField(default='0', max_length=1)

    def __str__(self):
        return f'{self.meme.Title}-{self.op}'


class Ring(models.Model):
    Post = models.ForeignKey(Meme, on_delete=models.CASCADE, default=3)
    Define = models.CharField(max_length=200)
    Defend = models.CharField(max_length=100, default="Aye")
    Attack = models.CharField(max_length=100, default="Nay")
    Creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f'{self.Define}-{self.Creator}'


class Msg(models.Model):
    op = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    time_stamp = models.DateTimeField(auto_now_add=True)
    cnt = models.TextField(max_length=500, default='Sorry an Error is here')
    ring = models.ForeignKey(Ring, on_delete=models.CASCADE, default=1)
    side = models.CharField(max_length=1, default='0')
    Edited = models.CharField(max_length=1, default='0')
    Edit_Time = models.DateTimeField(default=datetime.now())
    Edit_1 = models.TextField(max_length=500, default='')
    Edit_2 = models.TextField(max_length=500, default='')
    Reply = models.CharField(max_length=15, default='0')

    def __str__(self):
        return f'{self.op}-{self.cnt}'
