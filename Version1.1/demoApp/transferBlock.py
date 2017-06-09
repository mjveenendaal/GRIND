#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed May 31 10:37:03 2017

@author: LWR
"""

import laspy as las
from models import Point_Cloud, CacheFile
from django.http import HttpResponse#, HttpResponseForbidden
from django.views.decorators import csrf
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.contrib import messages# import get_messages
from django.conf import settings
import numpy as np
from scipy import spatial

def startTransfer(request):
    ctx = {}
    pcFiles = CacheFile.objects.all()
    if pcFiles:
        return HttpResponse('Hello')
        if request.method == 'POST':
            return HttpResponse(str(request.POST))
            if '_transfer' in request.POST:
                return HttpResponse('Hello')
                for f in pcFiles:
                    n = str(f.pc.name)[9:]
                    f = settings.MEDIA_ROOT + '/' + str(f.pc.name)
                    f = file.File(f, mode='r')
                    importances = np.random.exponential(0.5, len(f))
#        outfile.imp = np.random.exponential(0.5, len(infile))
                    for i in range(10000):
                        if 'X' in dir(f[i]) and 'Y' in dir(f[i]) and 'Z' in dir(f[i]):
                            p = Point_Cloud(x=f[i].X, y=f[i].Y, z=f[i].Z, imp=importances[i], name = n)
                            p.save()

    return render(request, 'index.html', ctx)