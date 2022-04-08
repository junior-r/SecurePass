from datetime import date
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.


class CreationUser(AbstractUser):
    picture_profile = models.ImageField(upload_to='Profiles', null=True, blank=True)

    def get_image(self):
        if self.picture_profile:
            return '{}{}'.format(settings.MEDIA_URL, self.picture_profile)
        else:
            pass


class CreatePassword(models.Model):
    password = models.CharField(max_length=50)
    website = models.URLField()
    creation_date = models.DateField(default=date.today)
    username = models.CharField(max_length=100)

    def __str__(self):
        return '{} {} {} {}'.format(self.username, self.password, self.website, self.creation_date)
