# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def viewer(request):
    return render(request, 'viewer.html')

def viewer_up(request):
    return render(request, 'viewer_up.html')