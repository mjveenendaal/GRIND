# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, render_to_response
from models import Upload_Form, Pic#, Name
from django.http import HttpResponse#, HttpResponseForbidden
from django.views.decorators import csrf
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages# import get_messages
from django.conf import settings

"""
The comments below are basically for debugging.
What's tricky about Django is that none of the variables within the if statement can be passed on for further use.
e.g. in my latest version, I replaced "p.save()" and "return HttpResponseRedirect(reverse('upload_pic'))" with the 43th line;
then when I checked the final output of ctx it remained empty.
"""
def index(request):
    return HttpResponse(request.method)

def upload_pic(request):
    ctx = {}
    if request.method == 'POST':
#        return HttpResponse(request.method)
        form = Upload_Form(request.POST, request.FILES)
#        return HttpResponse(request.FILES['UploadedFile'].name) #valid file but still invalid form
        if form.is_valid():
#            return HttpResponse(request.FILES['UploadedFile'])
            p = Pic(UploadedFile = request.FILES['UploadedFile'])
#            return HttpResponse(p)
            p.save()
#            n = Name(name = request.FILES['UploadedFile'].name)
#            n.save()
            return HttpResponseRedirect(reverse('upload_pic'))
        else:
            ctx['form'] = form
            return render(request, 'invalid.html', ctx)

#        form = Upload_Form() # An empty, unbound form
        
    p = Pic.objects.all()
#    n = Name.objects.all()
    ctx['p'] = p
#    return HttpResponse(p)
#    ctx['media'] = settings.MEDIA_ROOT + 'pic_folder/'
    return render(request, 'upload.html', ctx)