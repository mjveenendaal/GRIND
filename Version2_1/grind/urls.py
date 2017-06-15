#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views, uploadModule, downloadModule
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^upload-pc$', uploadModule.toUpload, name = 'upload_pc'),
    url(r'^download-pc$', downloadModule.toDownload, name = 'download_pc'),
    url(r'^viewer-pc$', views.viewer, name='viewer_pc'),
    url(r'^another-viewer-pc$', views.another_viewer, name='another_viewer_pc'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
