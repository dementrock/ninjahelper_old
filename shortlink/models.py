from django.db import models

# Create your models here.

class ShortLink(models.Model):
    user_profile = models.ForeignKey('community.UserProfile', related_name='shortlink')
    shortname = models.CharField(max_length=100)
    url = models.URLField(max_length=100)


