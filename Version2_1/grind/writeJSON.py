#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from django.core.serializers import serialize
from models import Point_Cloud
from django.http import HttpResponse#, HttpResponseForbidden
from django.views.decorators import csrf
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.contrib import messages# import get_messages
from django.conf import settings
from django.contrib.gis.geos import GEOSGeometry

def writeJSON(request):
    if request.method == 'POST':
        if '_viewer' in request.POST:
            return HttpResponse('hello')