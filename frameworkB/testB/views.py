# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, render_to_response
from models import Upload_Form, Pic, Download_Form, NameCache
from django.http import HttpResponse#, HttpResponseForbidden
from django.views.decorators import csrf
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages# import get_messages
from django.conf import settings
from download import ToDownload

def index(request):
    return HttpResponse(request.method)

def get_pic(request):
    if request.method == 'POST':
        if '_upload' in request.POST:
            form = Upload_Form(request.POST, request.FILES)
            if form.is_valid():
                p = Pic(UploadedFile = request.FILES['UploadedFile'], Name = request.FILES['UploadedFile'].name)
                p.save()
                Pic.objects.filter(id=p.id).update(Name=str(p.UploadedFile.name))
                return HttpResponseRedirect(reverse('get_pic'))
            else:
                return render(request, 'invalid.html', {'form':form})

        elif '_download' in request.POST:
            p = Pic.objects.all()
            #x = []
            form = Download_Form(request.POST or None)
            if form.is_valid():
                names = [str(f.UploadedFile.name) for f in p]
                selected = [str(s) for s in request.POST.keys()]
                #return HttpResponse(str(selected))
                for s in selected:
                    if s in names:
                        x = ToDownload(pic_name=s)
                        x.save(url='http://localhost:8000/media/'+s)
                        #return HttpResponse('HelloWorld')
                return HttpResponseRedirect(reverse('get_pic'))
                        #return HttpResponse(x.N)
            else:
                return render(request, 'invalid.html', {'form':form})
    
    p = Pic.objects.all()
    #x = NameCache.objects.all()
    #return HttpResponse(x[0].N)
    return render(request, 'upload.html', {'p':p})