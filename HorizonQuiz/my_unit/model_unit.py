from django.db import models


class Map(models.Model):
    bg = models.ForeignKey(Background)
    region = models.ForeignKey(Region)


class Background(models.Model):
    url = models.CharField(max_length=256)
    x = models.IntegerField
    y = models.IntegerField
    width = models.IntegerField
    height = models.IntegerField


class Region(models.Model):
    url = models.CharField(max_length=256)
    x = models.IntegerField
    y = models.IntegerField
    width = models.IntegerField
    height = models.IntegerField
    area = []
