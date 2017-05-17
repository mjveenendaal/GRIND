#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May  8 15:58:09 2017

@author: LWR
"""

from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static
#from . import download

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^get-pic$', views.get_pic, name = 'get_pic'),
    #url(r'^download-file$', download.download_file, name = 'download_file'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)