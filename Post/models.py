from django.db import models


# Create your models here.
class MemeImg(models.Model):
    Title = models.CharField(max_length=500)
    Post_Img = models.ImageField(upload_to='images/', blank=True)

    def __str__(self):
        return self.Title
