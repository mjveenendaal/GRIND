#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import laspy
from models import Point_Cloud
#from django.http import HttpResponse
from django.views.decorators import csrf
#from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.contrib import messages# import get_messages
from django.conf import settings
from django.contrib.gis.geos import GEOSGeometry
#from django.contrib.gis.gdal import SpatialReference, CoordTransform
#from django.core.serializers import serialize
import numpy as np
#import geojson

def toDownload(request):
    ctx = {}
    pointExist = Point_Cloud.objects.all()[:1]
    if pointExist:
        if request.POST:
            if '_download' in request.POST:
                #check which forms are filled in
                if request.POST['x'] and request.POST['y'] and request.POST['r']:
                    x0 = float(str(request.POST['x']))
                    y0 = float(str(request.POST['y']))
                    radius = float(str(request.POST['r']))
                elif request.POST['x'] and request.POST['y']:
                    x0 = float(str(request.POST['x']))
                    y0 = float(str(request.POST['y']))
                    radius = 459.494
                elif request.POST['y'] and request.POST['r']:
                    x0 = '85168.41'
                    y0 = float(str(request.POST['y']))
                    radius = float(str(request.POST['r']))
                elif request.POST['x'] and request.POST['r']:
                    x0 = float(str(request.POST['x']))
                    y0 = '446709.42'
                    radius = float(str(request.POST['r']))
                elif request.POST['x']:
                    x0 = float(str(request.POST['x']))
                    y0 = '446709.42'
                    radius = 459.494
                elif request.POST['y']:
                    x0 = '85168.41'
                    y0 = float(str(request.POST['y']))
                    radius = 459.494
                elif request.POST['r']:
                    x0 = '85168.41'
                    y0 = '446709.42'
                    radius = float(str(request.POST['r']))
                else:
                    x0 = '85168.41'
                    y0 = '446709.42'
                    radius = 459.494
                center = GEOSGeometry('SRID=28992;POINT (' + str(x0) +' '+ str(y0) + ')')
                polygon = center.buffer(radius)
                if request.POST['filename']:
                    f_name = str(request.POST['filename'])
                else:
                    f_name = 'downloadedpc'
                    
                outfile = laspy.file.File(settings.MEDIA_ROOT + '/' + f_name +'.las', mode='w', header=laspy.header.Header())

                outfile.define_new_dimension(name = "imp",
                        data_type = 9, description = "Importance value")
                temp1 = Point_Cloud.objects.values('id', 'imp', 'xypoint')
                temp2 = []
                for p in temp1:
                    if p['xypoint'].distance(center)/radius < p['imp']: #distance query
                        temp2.append(p['id'])
                #ST_Within query
                allx = np.array([x for x in Point_Cloud.objects.filter(xypoint__within = polygon, id__in = temp2).values_list('x', flat=True)])
                ally = np.array([y for y in Point_Cloud.objects.filter(xypoint__within = polygon, id__in = temp2).values_list('y', flat=True)])
                allz = np.array([z for z in Point_Cloud.objects.filter(xypoint__within = polygon, id__in = temp2).values_list('z', flat=True)])
                allimp = np.array([imp for imp in Point_Cloud.objects.filter(xypoint__within = polygon, id__in = temp2).values_list('imp', flat=True).order_by('imp')])

                outfile.X = allx
                outfile.Y = ally
                outfile.Z = allz
                outfile.imp = allimp
                outfile.header.offset = [min(allx), min(ally), min(allz), min(allimp)]
                outfile.header.scale = [0.001,0.001,0.001, 0.001]
                outfile.close()
                ctx['done'] = 'File ' + f_name + ' is downloaded!'

            elif '_viewer' in request.POST:
                if request.POST['x'] and request.POST['y'] and request.POST['r']:
                    x0 = float(str(request.POST['x']))
                    y0 = float(str(request.POST['y']))
                    radius = float(str(request.POST['r']))
                elif request.POST['x'] and request.POST['y']:
                    x0 = float(str(request.POST['x']))
                    y0 = float(str(request.POST['y']))
                    radius = 459.494
                elif request.POST['y'] and request.POST['r']:
                    x0 = '85168.41'
                    y0 = float(str(request.POST['y']))
                    radius = float(str(request.POST['r']))
                elif request.POST['x'] and request.POST['r']:
                    x0 = float(str(request.POST['x']))
                    y0 = '446709.42'
                    radius = float(str(request.POST['r']))
                elif request.POST['x']:
                    x0 = float(str(request.POST['x']))
                    y0 = '446709.42'
                    radius = 459.494
                elif request.POST['y']:
                    x0 = '85168.41'
                    y0 = float(str(request.POST['y']))
                    radius = 459.494
                elif request.POST['r']:
                    x0 = '85168.41'
                    y0 = '446709.42'
                    radius = float(str(request.POST['r']))
                else:
                    x0 = '85168.41'
                    y0 = '446709.42'
                    radius = 459.494
                center = GEOSGeometry('SRID=28992;POINT (' + str(x0) +' '+ str(y0) + ')')
                polygon = center.buffer(radius)
                
                temp1 = Point_Cloud.objects.values('id', 'imp', 'xypoint')
                temp2 = []
                for p in temp1:
                    if p['xypoint'].distance(center)/radius < p['imp']:#**2:
                        temp2.append(p['id'])
                selected = Point_Cloud.objects.filter(xypoint__within = polygon, id__in = temp2).order_by('imp')

                points = []
                
                for i in range(len(selected)):
                    points.append(selected[i].x)
                    points.append(selected[i].y)
                    points.append(selected[i].z)
                    points.append(selected[i].imp)

                string = 'var visualisation = ' + str(points) + ';\n' + 'var centre = ' + str([x0, y0, 0.0]) + ';'
                outfile = file(settings.MEDIA_ROOT + '/visualisation.js', mode='w')                
                outfile.write(string)
                outfile.close()
                ctx['done'] = 'File is ready for the viewer!'
    else:
        ctx['done'] = 'No point cloud available!'
        return render(request, 'upload.html', ctx)
    return render(request, 'download.html', ctx)