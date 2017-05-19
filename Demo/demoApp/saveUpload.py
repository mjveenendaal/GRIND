#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May 18 00:05:06 2017

@author: LWR
"""

from laspy import file
from models import UploadForm, Point_Cloud, CacheFile
from django.http import HttpResponse#, HttpResponseForbidden
from django.views.decorators import csrf
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.contrib import messages# import get_messages
from django.conf import settings
import os

def saveUpload(request):
    ctx = {}
    if request.method == 'POST':
        if '_upload' in request.POST:
            form = UploadForm(request.POST, request.FILES) #input from html
            if form.is_valid():
                f = CacheFile(pc = request.FILES['pc']) #save file for las attributes retrieval
                if str(f.pc.name).endswith('.las'):
                    f.save()
                    n = str(f.pc.name)[9:]
                    f = settings.MEDIA_ROOT + '/' + str(f.pc.name)
                    f = file.File(f, mode='r') #apply laspy
                    for i in range(10000):
                        if 'X' in dir(f[i]) and 'Y' in dir(f[i]) and 'Z' in dir(f[i]):
                            p = Point_Cloud(x=f[i].X, y=f[i].Y, z=f[i].Z, name = n)
                            p.save()
                    return HttpResponseRedirect(reverse('upload_pc'))
            else:
                ctx['form'] = form
                return render(request, 'index.html', ctx)
    if CacheFile.objects.all():
        ctx['message'] = 'Saved!'
        CacheFile.objects.all().delete() #otherwise the message keeps being alerted
        n = [str(nn['name']) for nn in Point_Cloud.objects.values('name').distinct()]
        for name in n:
            os.remove(settings.MEDIA_ROOT + '/pc_cache/' + name)
    return render(request, 'index.html', ctx)