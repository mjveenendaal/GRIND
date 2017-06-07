#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May  8 15:58:09 2017

@author: LWR
"""

from django.conf.urls import url
from . import views, saveUpload, downloadBlock
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^upload-pc$', saveUpload.saveUpload, name = 'upload_pc'),
    url(r'^download-pc$', downloadBlock.toDownload, name = 'download_pc'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)