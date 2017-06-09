# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView

def index(request):
    return render(request, 'main.html')

class ViewerPageView(TemplateView):
    template_name = "viewer.html"

#def viewer(request):
#    return render(request, 'viewer.html')
