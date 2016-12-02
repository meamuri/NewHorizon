from django.db import models


class Map(models.Model):
    url = models.CharField(max_length=256, default='default')
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    width = models.IntegerField(default=100)
    height = models.IntegerField(default=100)

    def __str__(self):
        return self.url + ' x: ' + str(self.x) + ' y: ' + str(self.y)


class RegionType(models.Model):
    url = models.CharField(max_length=256, default='none')
    name = models.CharField(max_length=128, default='')
    width = models.IntegerField(default=0)
    height = models.IntegerField(default=0)

    def __str__(self):
        return self.name + " width: " + str(self.width) + " height: " + str(self.height)


class Region(models.Model):
    x = models.IntegerField(default=0)  # позиция на карте относительно размера самой карты (как коэффициент) 0..100
    y = models.IntegerField(default=0)  # позиция на карте относительно размера самой карты (как коэффициент) 0..100
    reg_type = models.ForeignKey(RegionType, default=1)
    area = models.CharField(max_length=1024)
    map = models.ForeignKey(Map, default=1)
    is_capital_area = models.BooleanField(default=False)

    owner_id = 0

    def get_collection_of_area_as_strings(self, screen_width=1, screen_height=1):
        res = []
        points = self.area.split('--')
        for pnt in points:
            res.append({
                'x': int(pnt[:pnt.index(';')]) * screen_width / 100,
                'y': int(pnt[pnt.index(';') + 1:]) * screen_height / 100
            })
        return res

    def __str__(self):
        return self.reg_type.url + " x: " + str(self.x) + " y: " + str(self.y)

    def sizes(self):
        return {"width": self.reg_type.width, "height": self.reg_type.height}

    def position(self, screen_width=1, screen_height=1):
        return {"x": self.x*screen_width/100, "y": self.y*screen_height/100}


def get_play_map_as_dict(map_id, width, height):
    """
    Получение игровой карты, содержащей информацию для отображения на экране игрового устройства
    :param map_id:  id картый, с которой связаны регионы
    :param width:   ширина игрового экрана пользователя
    :param height:  высота игрового экрана пользователя
    :return: Словарь, содержащий пары "ключ - значения", связанные с данными о :
        - положении регионов на экране
        - набор точек, обрамляющих каждый регион
        - набор размеров этих регионов
        - типы этих регионов (столица, или нейтральная)
    """
    lst_areas = []
    lst_pos = []
    lst_sizes = []
    lst_urls = []
    lst_types = []

    fill_regions_info(map_id, lst_areas, lst_pos, lst_sizes, lst_urls, lst_types, width, height)

    return {
        'region-poses': lst_pos,
        'region-areas': lst_areas,
        'region-sizes': lst_sizes,
        'region-types': lst_types,
    }


def get_regions_as_list(map_id, player, his_enemy):
    """
    Получение набора регионов в виде списка. Список необходим для
    :param map_id:      Регионы какой карты необходимо получить
    :param player:      Игрок, для которого запрашивается набор регионов
    :param his_enemy:   Его соперник
    :return:            Список, содержащий объекты класса Region, инициализированные
        данными о принадлежности этих регионов игрокам
        данными о том, являются ли они столичными
    """
    res = []
    for obj in Region.objects.all():
        if obj.map_id == map_id:
            res.append(obj)
            res[-1].owner_id = -1
    res[0].is_capital_area = res[-1].is_capital_area = True
    res[0].owner_id = player
    res[-1].owner_id = his_enemy
    return res


def fill_regions_info(num, areas, poses, sizes, urls, types, width=1, height=1):
    """
    Функция, заполняющая переданные в качестве параметра списки данными о карте
    и составляющих ее регионах
    :param num:     id той карты, которой принадлежат регионы
    :param areas:   список регионов
    :param poses:   положения их на игровом экране
    :param sizes:   размеры регионов на экране
    :param urls:    адреса картинок, связанных с ними
    :param types:   типы этих регионов - столица ли?
    :param width:   ширина экрана игрового устройства
    :param height:  высота экрана игрого устройства
    :return: None
    """
    for a in Region.objects.all():
        if a.map_id == num:
            areas.append(a.get_collection_of_area_as_strings(width, height))
            poses.append(a.position(width, height))
            sizes.append(a.sizes())
            urls.append(a.reg_type.url)
            if a.is_capital_area:
                types.append(1)
            else:
                types.append(0)
