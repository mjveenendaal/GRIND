# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django import forms

class Upload_Form(forms.Form):
    UploadedFile = forms.FileField(label='Select a file',)
    
class Pic(models.Model):
    UploadedFile = models.FileField(upload_to='', default='DEFAULT VALUE', blank=True, null=True)
    Name = models.CharField(max_length=200, null=True)
    
class Download_Form(forms.Form):
    Choices = forms.BooleanField(required=False)
    
class NameCache(models.Model):
    N = models.CharField(max_length=200, null=True)