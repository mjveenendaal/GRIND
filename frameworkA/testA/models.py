# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django import forms

class Upload_Form(forms.Form):
    UploadedFile = forms.FileField(label='Select a file',)#The definitions have to be the same as the HTML input
    #e.g. <input name="whatever">, so here we define the variable whatever.
    
class Pic(models.Model):
    UploadedFile = models.FileField(upload_to = 'pic_folder/', default='DEFAULT VALUE', blank=True, null=True)
    
#class Name(models.Model):
#    pic = models.ForeighKey(Pic, on_delete = models.CASCADE)
#    name = models.CharField(max_length = 100)
#    def __str__(self):
#        return self.name
