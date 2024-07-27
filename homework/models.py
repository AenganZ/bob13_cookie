from django.db import models


class User(models.Model):
    userid = models.CharField(max_length=10)
    userpw = models.CharField(max_length=15)
    sessionid = models.CharField(max_length=256, null=True, blank=True)