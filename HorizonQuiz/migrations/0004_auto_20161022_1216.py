# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-22 11:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HorizonQuiz', '0003_background_region'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Background',
            new_name='Map',
        ),
    ]
