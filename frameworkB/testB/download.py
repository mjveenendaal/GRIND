#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed May 10 11:41:35 2017

@author: Nikhil Haas in Programming, Web
@Source: http://ishcray.com/downloading-and-saving-image-to-imagefield-in-django

@Modified by GRIND team

The validation process is removed from the original codes because image is only used as a test
"""

from django.db import models
import urllib2
import urlparse
import cStringIO #imitate reading from byte file; written in C for speed
from PIL import Image
import os
from django.core.files.base import ContentFile
#from django.http import HttpResponse #for debugging purpose

class ToDownload(models.Model):
    pic_name = models.CharField('Name', max_length=200)
    pict = models.ImageField('Picture', upload_to='pic/', null=True, blank=True)
    def save(self, url='', *args, **kwargs):
        if self.pict != '' and url != '':
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0'}
            r = urllib2.Request(url, headers=headers)
            request = urllib2.urlopen(r, timeout=10)
            image_data = cStringIO.StringIO(request.read())
            image = Image.open(image_data) #an instance of PIL Image is created
            try:
                filename = urlparse.urlparse(url).path.split(os.sep)[-1]
                self.pict = filename
                tempfile = image
                tempfile_io = cStringIO.StringIO()
                tempfile.save(tempfile_io, format=image.format)
                self.pict.save(filename, ContentFile(tempfile_io.getvalue()), save=False) #to avoid a loop of save method
            except Exception, e:
                print "Error"+str(e)
                pass
            super(ToDownload, self).save(*args, **kwargs) #gets the parent of this class and run the normal save method
