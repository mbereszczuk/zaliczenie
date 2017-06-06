from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import smart_unicode


class MainCategory(models.Model):
    name = models.CharField(max_length=63)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    bal = models.FloatField()
    def __unicode__(self):
        return smart_unicode(self.name)

class Entry(models.Model):
    type = models.CharField(max_length=2, choices=[("p","przychod"),("w","wydatek")])
    value = models.FloatField()
    date = models.DateField()
    description = models.CharField(max_length=255)
    user = models.ForeignKey(User)
    category = models.ForeignKey(MainCategory, on_delete = models.CASCADE)
