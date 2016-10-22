from django.contrib import admin

# Register your models here.
from .models import Question, AccuracyQuestion
from HorizonQuiz.my_unit.model_unit import Region


admin.site.register(Question)
admin.site.register(AccuracyQuestion)
admin.site.register(Region)
