from django.db import models


class Map(models.Model):
    url = models.CharField(max_length=256, default='default')
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    width = models.IntegerField(default=100)
    height = models.IntegerField(default=100)

    def __str__(self):
        return self.url + ' x: ' + str(self.x) + ' y: ' + str(self.y)


class Region(models.Model):
    url = models.CharField(max_length=256, default='none')
    x = models.IntegerField(default=0)  # позиция на карте относительно размера самой карты (как коэффициент) 0..100
    y = models.IntegerField(default=0)  # позиция на карте относительно размера самой карты (как коэффициент) 0..100
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    area = models.CharField(max_length=1024)
    map = models.ForeignKey(Map, default=1)

    def get_collection_of_area_as_strings(self):
        return self.area.split('--')

    def __str__(self):
        return self.url + " x: " + str(self.x) + " y: " + str(self.y)

    def sizes(self):
        return str(self.width) + ';' + str(self.height)

    def position(self):
        return str(self.x) + ';' + str(self.y)
