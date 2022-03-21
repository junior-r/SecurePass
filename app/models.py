from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class CreatePassword(models.Model):
    password = models.CharField(max_length=50)
    website = models.URLField()
    creation_date = models.DateTimeField(auto_now=True)
    username = models.CharField(max_length=100)

    def __str__(self):
        return '{} {} {} {}'.format(self.username, self.password, self.website, self.creation_date)
