# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django import forms
import django.contrib.gis.db.models

class UploadForm(forms.Form):
    pc = forms.FileField(label='Select a file')
    
class CacheFile(models.Model):
    pc = models.FileField(upload_to='pc_cache/', default='DEFAULT VALUE', blank=True, null=True)
    
class Point_Cloud(models.Model):
    x = models.FloatField(default=0)
    y = models.FloatField(default=0)
    z = models.FloatField(default=0)
    imp = models.FloatField(default=0)
#    name = models.CharField(max_length=200, null=True) #names of multiple files can be saved here
    xypoint = django.contrib.gis.db.models.GeometryField(srid=28992, null=True)