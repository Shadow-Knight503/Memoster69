from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField as BaseCloudinaryField


# Create your models here.
class CloudinaryField(BaseCloudinaryField):
    def upload_options(self, model_instance):
        return {
            'unique_filename': False,
            'overwrite': True,
            'resource_type': 'image',
            'tags': ['Profile'],
            'invalidate': True,
            'quality': 'auto:eco',
        }


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    Nick_Name = models.CharField(default="Hey", max_length=250)
    Profile_pic = CloudinaryField('Profile_Pic', overwrite=True)

    def __str__(self):
        return self.user.username


class Theme(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    Name = models.CharField(max_length=100, default="Cool Theme?")
    Nav_Back = models.CharField(default="#020440", max_length=10)
    Nav_Color = models.CharField(default="#d8c70e", max_length=10)
    Nav_Line = models.CharField(default="#d8c70e", max_length=10)
    Body_Back = models.CharField(default="#2d2424", max_length=10)
    Card_Back = models.CharField(default="#2d2424", max_length=10)
    Card_Color = models.CharField(default="#ffffff", max_length=10)
    Card_Border = models.CharField(default="#020440", max_length=10)

    def __str__(self):
        return f"{self.user.user.username}-{self.Name}"
