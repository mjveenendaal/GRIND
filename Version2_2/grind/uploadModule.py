#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from laspy import file
from models import UploadForm, Point_Cloud, CacheFile
#from django.http import HttpResponse # for debug purpose: print intermediate results on screen
from django.views.decorators import csrf
#from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.contrib import messages
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
                if str(f.pc.name).endswith('.las'): #only las. files will be proceeded
                    f.save()
                    ctx['uploaded'] = 'File ' + str(f.pc.name)[9:] + ' is uploaded!'
                    return render(request, 'upload.html', ctx)
            else:
                ctx['form'] = form
                return render(request, 'upload.html', ctx)
        elif '_transfer' in request.POST: #once the button is clicked
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
                    importances = np.random.exponential(0.5, len(f)) #random assignment of importance values; another two importance assignments
                    #are in this folder, and can be copied and pasted here
                    stringPoints =  StringIO()
                    w = csv.writer(stringPoints) 
                    data = []
                    conn = psycopg2.connect(host='localhost', port='5432', dbname=#name of the database, user='postgres', password=#password of the database)
                    cur = conn.cursor()
                    pointExist = Point_Cloud.objects.all()[:1]
                    if pointExist:
                        id_start = Point_Cloud.objects.all().aggregate(Max('id'))['id__max']+1
                    else:
                        id_start = 0
                    for i in range(len(f)):
                        if 'X' in dir(f[i]) and 'Y' in dir(f[i]) and 'Z' in dir(f[i]):
                            coefficient = 10**(5-len(str(f[i].X))) #coordinates in the las. file are integers; regularise them into RD CRS first
                            point_list = [i+id_start, f[i].X*coefficient, f[i].Y*coefficient, f[i].Z*coefficient, importances[i], GEOSGeometry('SRID=28992;POINT ('+str(f[i].X*coefficient)
                                            +' '+str(f[i].Y*coefficient)+')')]		
                            data.append(point_list)
                            if i % 100000 == 0 and i > 0: #save points in patches of every 0.1M
                                w.writerows(data)
                                stringPoints.seek(0)
                                cur.copy_from(stringPoints, "grind_point_cloud", sep=',', columns=('id', 'x', 'y', 'z', 'imp', 'xypoint'))#, 'xyzpoint')) 
                                stringPoints.close()
                                stringPoints = StringIO()
                                w = csv.writer(stringPoints) 
                                data = []
                                j = i/100000
                            
                    conn.commit()
                    stringPoints.close()
                    stringPoints = StringIO()
                    w = csv.writer(stringPoints) 
                    data = []

                    for i in range(j*100000+1, len(f)): #save outlying points
                        coefficient = 10**(5-len(str(f[i].X)))
                        point_list = [i+id_start, f[i].X*coefficient, f[i].Y*coefficient, f[i].Z*coefficient, importances[i], GEOSGeometry('SRID=28992;POINT ('+str(f[i].X*coefficient)
                                            +' '+str(f[i].Y*coefficient)+')')]
		
                        data.append(point_list)
    
                        w.writerows(data)

                        stringPoints.seek(0)
                        cur.copy_from(stringPoints, "grind_point_cloud", sep=',', columns=('id', 'x', 'y', 'z', 'imp', 'xypoint')) 

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
    return render(request, 'upload.html', ctx)
