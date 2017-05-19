# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django import forms

class UploadForm(forms.Form):
    pc = forms.FileField(label='Select a file')
    
class CacheFile(models.Model):
    pc = models.FileField(upload_to='pc_cache/', default='DEFAULT VALUE', blank=True, null=True)
    
class Point_Cloud(models.Model):
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    z = models.IntegerField(default=0)
    name = models.CharField(max_length=200, null=True)