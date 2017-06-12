#!/usr/bin/env python2
# -*- coding: utf-8 -*-

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
                    f_name = str(request.POST['filename'])
                else:
                    f_name = '/downloadedpc'
                    
                outfile = laspy.file.File(settings.MEDIA_ROOT + '/' + f_name +'.las', mode='w', header=laspy.header.Header())

                outfile.define_new_dimension(name = "imp",
                        data_type = 9, description = "Importance value")
                temp1 = Point_Cloud.objects.values('id', 'imp', 'xypoint')
                temp2 = []
                for p in temp1:
                    if p['xypoint'].distance(center)/radius < p['imp']:
                        temp2.append(p['id'])
                total = int(len(temp2) * percentage)
                allx = np.array([x for x in Point_Cloud.objects.filter(xypoint__within = polygon, id__in = temp2).values_list('x', flat=True).order_by('imp')])[:total]
                ally = np.array([y for y in Point_Cloud.objects.filter(xypoint__within = polygon, id__in = temp2).values_list('y', flat=True).order_by('imp')])[:total]
                allz = np.array([z for z in Point_Cloud.objects.filter(xypoint__within = polygon, id__in = temp2).values_list('z', flat=True).order_by('imp')])[:total]
                allimp = np.array([imp for imp in Point_Cloud.objects.filter(xypoint__within = polygon, id__in = temp2).values_list('imp', flat=True).order_by('imp')])[:total]

                outfile.X = allx
                outfile.Y = ally
                outfile.Z = allz
                outfile.imp = allimp
                outfile.header.offset = [min(allx), min(ally), min(allz), min(allimp)]
                outfile.header.scale = [0.001,0.001,0.001, 0.001]
                outfile.close()
                ctx['done'] = 'File ' + f_name[9:] + ' is downloaded!'
    else:
        ctx['done'] = 'No point cloud available!'
#        return render(request, 'upload.html', ctx)
    return render(request, 'download.html', ctx)