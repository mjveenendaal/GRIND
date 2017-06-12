#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 16:38:09 2017

@author: LWR
"""

def decimalConverter(n0, n):
    p0 = str(n0).find('.')
    p = str(n).find('.')
    if p == -1:
        return 10**(p0-len(str(n0))+1)
    else:
        return 0