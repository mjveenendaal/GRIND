#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from laspy import file
from models import UploadForm, Point_Cloud, CacheFile
from django.http import HttpResponse#, HttpResponseForbidden
from django.views.decorators import csrf
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.contrib import messages# import get_messages
from django.conf import settings
from django.contrib.gis.geos import GEOSGeometry
from django.db.models import Max
#import os
import numpy as np
from cStringIO import StringIO
import csv
import psycopg2

def toUpload(request):
    ctx = {}
    if request.method == 'POST':
        if '_upload' in request.POST:
            form = UploadForm(request.POST, request.FILES) #input from html
            if form.is_valid():
                f = CacheFile(pc = request.FILES['pc']) #save file for las attributes retrieval
                if str(f.pc.name).endswith('.las'):
                    f.save()
                    ctx['uploaded'] = 'File ' + str(f.pc.name)[9:] + ' is uploaded!'
                    return render(request, 'upload.html', ctx)
            else:
                ctx['form'] = form
                return render(request, 'upload.html', ctx)
        elif '_transfer' in request.POST:
            pcFiles = CacheFile.objects.all()
            if pcFiles:
                for f in pcFiles:
#                    n = str(f.pc.name)[9:]
                    f_name = settings.MEDIA_ROOT + '/' + str(f.pc.name)
                    try:
                        f = file.File(f_name, mode='r')
                    except:
                        ctx['error'] = 'File ' + str(f.pc.name)[9:] + ' does not exist!'
                        CacheFile.delete(f)
                        return render(request, 'upload.html', ctx)
                    importances = np.random.exponential(0.5, len(f))
                    stringPoints =  StringIO()
                    w = csv.writer(stringPoints) 
                    data = []
                    conn = psycopg2.connect(host='localhost', port='5431', dbname='grind', user='postgres', password='950206')
                    cur = conn.cursor()
                    pointExist = Point_Cloud.objects.all()[:1]
                    if pointExist:
                        id_start = Point_Cloud.objects.all().aggregate(Max('id'))['id__max']+1
                    else:
                        id_start = 0
#        outfile.imp = np.random.exponential(0.5, len(infile))
                    for i in range(len(f)):
                        if 'X' in dir(f[i]) and 'Y' in dir(f[i]) and 'Z' in dir(f[i]):
                            coefficient = 10**(5-len(str(f[i].X)))
#                            p = Point_Cloud(x=f[i].X, y=f[i].Y, z=f[i].Z, 
#                                            imp=importances[i], name = n, 
#                                            xypoint=GEOSGeometry('SRID=28992;POINT ('+str(f[i].X*0.01)
#                                            +' '+str(f[i].Y*0.01)+')'))
#                            p.save()
                            point_list = [i+id_start, f[i].X*coefficient, f[i].Y*coefficient, f[i].Z*coefficient, importances[i], GEOSGeometry('SRID=28992;POINT ('+str(f[i].X*coefficient)
                                            +' '+str(f[i].Y*coefficient)+')')]#, GEOSGeometry('SRID=28992;POINT ('+str(f[i].X*coefficient)
#                                            +' '+str(f[i].Y*coefficient)+' '+str(f[i].Z*coefficient)+')')]		
                            data.append(point_list)
                            if i % 100000 == 0 and i > 0:
                                w.writerows(data)
                                stringPoints.seek(0)
                                cur.copy_from(stringPoints, "grind_point_cloud", sep=',', columns=('id', 'x', 'y', 'z', 'imp', 'xypoint'))#, 'xyzpoint')) 
                                stringPoints.close()
                                stringPoints = StringIO()
                                w = csv.writer(stringPoints) 
                                data = []
                                j = i/100000
                            
                    #w.writerows(data)
                    #stringPoints.seek(0)
                    #cur.copy_from(stringPoints, 'pointcloud3', sep=',', columns=('id', 'x', 'y', 'z', 'imp'))
                    conn.commit()
                    stringPoints.close()
                    stringPoints = StringIO()
                    w = csv.writer(stringPoints) 
                    data = []

                    for i in range(j*100000+1, len(f)):
                        coefficient = 10**(5-len(str(f[i].X)))
                        point_list = [i+id_start, f[i].X*coefficient, f[i].Y*coefficient, f[i].Z*coefficient, importances[i], GEOSGeometry('SRID=28992;POINT ('+str(f[i].X*coefficient)
                                            +' '+str(f[i].Y*coefficient)+')')]#, GEOSGeometry('SRID=28992;POINT ('+str(f[i].X*coefficient)
#                                            +' '+str(f[i].Y*coefficient)+' '+str(f[i].Z*coefficient)+')')]
		
                        data.append(point_list)
    
                        w.writerows(data)

                        stringPoints.seek(0)
                        cur.copy_from(stringPoints, "grind_point_cloud", sep=',', columns=('id', 'x', 'y', 'z', 'imp', 'xypoint'))#, 'xyzpoint')) 

                        stringPoints.close()
                        stringPoints = StringIO()
                        w = csv.writer(stringPoints) 
                        data = []
                    conn.commit()

                    # Close the writer and the database connection
                    conn.close()
                    stringPoints.close()
                    f.close()
            else:
                ctx['nothing'] = 'No data to transfer!'
#    if CacheFile.objects.all():
#        ctx['message'] = 'Saved!'
#        CacheFile.objects.all().delete() #otherwise the message keeps being alerted
#        n = [str(nn['name']) for nn in Point_Cloud.objects.values('name').distinct()]
#        for name in n:
#            os.remove(settings.MEDIA_ROOT + '/pc_cache/' + name)
    return render(request, 'upload.html', ctx)
