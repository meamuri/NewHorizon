from django.db import models


class Background(models.Model):
    url = models.CharField(max_length=256)
    x = models.IntegerField
    y = models.IntegerField
    width = models.IntegerField
    height = models.IntegerField


class Region(models.Model):
    url = models.CharField(max_length=256, default='none')
    x = models.IntegerField(default=0)  # позиция на карте относительно размера самой карты (как коэффициент) 0..100
    y = models.IntegerField(default=0)  # позиция на карте относительно размера самой карты (как коэффициент) 0..100
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    area = models.CharField(max_length=1024)

    def get_collection_of_area_as_strings(self):
        return self.area.split(';')

    def __str__(self):
        return self.url + str(self.x) + str(self.y)

    def sizes(self):
        return str(self.width) + '.' + str(self.height)

    def position(self):
        return str(self.x) + '.' + str(self.y)
