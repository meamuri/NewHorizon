# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-01 10:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HorizonQuiz', '0002_question_true_answer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='true_answer',
            field=models.IntegerField(default=1),
        ),
    ]