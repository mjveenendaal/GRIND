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
from django.contrib.gis.geos import GEOSGeometry
import numpy as np

def toDownload(request):
    ctx = {}
    pointExist = Point_Cloud.objects.all()[:1]
    #allPoints = Point_Cloud.objects.values_list('xypoint', flat=True).order_by('id')
    if pointExist:
        if request.POST:
            if '_download' in request.POST:
                if request.POST['percentage'] and float(str(request.POST['percentage'])) < 100:
                    percentage = float(str(request.POST['percentage'])) * 0.01
                else:
                    percentage = 1
                if request.POST['x'] and request.POST['y'] and request.POST['r']:
                    x0 = str(request.POST['x'])
                    y0 = str(request.POST['y'])
                    radius = str(request.POST['r'])
                elif request.POST['x'] and request.POST['y']:
                    x0 = str(request.POST['x'])
                    y0 = str(request.POST['y'])
                    radius = 459.494
                elif request.POST['y'] and request.POST['r']:
                    x0 = '85168.41'
                    y0 = str(request.POST['y'])
                    radius = str(request.POST['r'])
                elif request.POST['x'] and request.POST['r']:
                    x0 = str(request.POST['x'])
                    y0 = '446709.42'
                    radius = str(request.POST['r'])
                elif request.POST['x']:
                    x0 = str(request.POST['x'])
                    y0 = '446709.42'
                    radius = 459.494
                elif request.POST['y']:
                    x0 = '85168.41'
                    y0 = str(request.POST['y'])
                    radius = 459.494
                elif request.POST['r']:
                    x0 = '85168.41'
                    y0 = '446709.42'
                    radius = str(request.POST['r'])
                else:
                    x0 = '85168.41'
                    y0 = '446709.42'
                    radius = 459.494
                center = GEOSGeometry('SRID=28992;POINT (' + x0 +' '+ y0 + ')')
                polygon = center.buffer(radius)

#                if request.POST['density']:
#                    density = int(str(request.POST['density']))
#                    if density != 0:
#                        idList = []
#                        for pointId in allPointsId:
#                            if pointId % density == 0:
#                                idList.append(pointId)
#                    else:
#                        idList = [point for point in allPointsId]
#                else:
#                    idList = [point for point in allPointsId]
                #return HttpResponse(str(idList))
                if request.POST['filename']:
                    outfile = laspy.file.File(settings.MEDIA_ROOT + '/' + str(request.POST['filename'])+'.las', mode='w', header=laspy.header.Header())
                else:
                    outfile = laspy.file.File(settings.MEDIA_ROOT + '/downloadedpc.las', mode='w', header=laspy.header.Header())
                #return HttpResponse(str([p for p in Point_Cloud.objects.filter(id__in = idList).values_list('x', flat=True).order_by('id')]))
                outfile.define_new_dimension(name = "imp",
                        data_type = 9, description = "Importance value")
                temp1 = Point_Cloud.objects.values('id', 'imp', 'xypoint')
                temp2 = []
                for p in temp1:
                    if p['xypoint'].distance(center)/radius < p['imp']:
                        temp2.append(p['id'])
#                temp3 = [p for p in Point_Cloud.objects.filter(imp__in = temp2)]
                total = int(len(temp2) * percentage)
                allx = np.array([x for x in Point_Cloud.objects.filter(xypoint__within = polygon, id__in = temp2).values_list('x', flat=True).order_by('imp')])[:total]
                ally = np.array([y for y in Point_Cloud.objects.filter(xypoint__within = polygon, id__in = temp2).values_list('y', flat=True).order_by('imp')])[:total]
                allz = np.array([z for z in Point_Cloud.objects.filter(xypoint__within = polygon, id__in = temp2).values_list('z', flat=True).order_by('imp')])[:total]
                allimp = np.array([imp for imp in Point_Cloud.objects.filter(xypoint__within = polygon, id__in = temp2).values_list('imp', flat=True).order_by('imp')])[:total]
#                allx = np.array([x for x in Point_Cloud.objects.filter(xypoint__within = polygon, imp__gt = Point_Cloud.objects.values('xypoint').distance(center)).values_list('x', flat=True).order_by('id')])
#                ally = np.array([y for y in Point_Cloud.objects.filter(xypoint__within = polygon, imp__gt = 'xypoint'.distance(center)).values_list('y', flat=True).order_by('id')])
#                allz = np.array([z for z in Point_Cloud.objects.filter(xypoint__within = polygon, imp__gt = 'xypoint'.distance(center)).values_list('z', flat=True).order_by('id')])
#                allimp = np.array([imp for imp in Point_Cloud.objects.filter(xypoint__within = polygon, imp__gt = 'xypoint'.distance(center)).values_list('imp', flat=True).order_by('id')])
                #return HttpResponse(str(allx))
                outfile.X = allx
                outfile.Y = ally
                outfile.Z = allz
                outfile.imp = allimp
                outfile.header.offset = [min(allx), min(ally), min(allz), min(allimp)]
                #return HttpResponse(str(outfile.header.offset))
                outfile.header.scale = [0.001,0.001,0.001, 0.001]
                outfile.close()
    else:
        ctx['done'] = 'No point cloud available!'
    return render(request, 'viewing.html', ctx)