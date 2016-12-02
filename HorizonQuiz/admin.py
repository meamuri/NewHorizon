from django.contrib import admin
from .models import Question, AccuracyQuestion
from HorizonQuiz.my_unit.map_model import *


admin.site.register(Question)
admin.site.register(AccuracyQuestion)
admin.site.register(Region)
admin.site.register(Map)
admin.site.register(RegionType)
