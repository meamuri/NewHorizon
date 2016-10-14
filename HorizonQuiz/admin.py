from django.contrib import admin

# Register your models here.
from .models import Question, AccuracyQuestion

admin.site.register(Question)
admin.site.register(AccuracyQuestion)
