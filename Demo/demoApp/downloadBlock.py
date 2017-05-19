#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri May 19 09:38:38 2017

@author: LWR
"""

import laspy
from models import Point_Cloud
from django.http import HttpResponse#, HttpResponseForbidden
from django.views.decorators import csrf
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.contrib import messages# import get_messages
from django.conf import settings
import numpy as np

def toDownload(request):
    ctx = {}
    allPointsId = Point_Cloud.objects.values_list('id', flat=True).order_by('id')
    if allPointsId:
        if request.POST:
            if '_download' in request.POST:
                if request.POST['density']:
                    density = int(str(request.POST['density']))
                    if density != 0:
                        idList = []
                        for pointId in allPointsId:
                            if pointId % density == 0:
                                idList.append(pointId)
                    else:
                        idList = [point for point in allPointsId]
                else:
                    idList = [point for point in allPointsId]
                #return HttpResponse(str(idList))
                if request.POST['filename']:
                    outfile = laspy.file.File(settings.MEDIA_ROOT + '/' + str(request.POST['filename'])+'.las', mode='w', header=laspy.header.Header())
                else:
                    outfile = laspy.file.File(settings.MEDIA_ROOT + '/downloadedpc.las', mode='w', header=laspy.header.Header())
                #return HttpResponse(str([p for p in Point_Cloud.objects.filter(id__in = idList).values_list('x', flat=True).order_by('id')]))
                allx = np.array([x for x in Point_Cloud.objects.filter(id__in = idList).values_list('x', flat=True).order_by('id')])
                ally = np.array([y for y in Point_Cloud.objects.filter(id__in = idList).values_list('y', flat=True).order_by('id')])
                allz = np.array([z for z in Point_Cloud.objects.filter(id__in = idList).values_list('z', flat=True).order_by('id')])
                #return HttpResponse(str(allx))
                outfile.X = allx
                outfile.Y = ally
                outfile.Z = allz
                outfile.header.offset = [min(allx),min(ally),min(allz)]
                #return HttpResponse(str(outfile.header.offset))
                outfile.header.scale = [0.001,0.001,0.001]
                outfile.close()
    else:
        ctx['done'] = 'No point cloud available!'
    return render(request, 'viewing.html', ctx)