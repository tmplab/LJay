#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# -*- mode: Python -*-

'''
Laser Jaying

example code for compo laser at coockie 2018 demoparty

LICENCE : CC
Sam Neurohack, Loloster, 


'''


import math
import gstt
from globalVars import *
import colorify
from datetime import datetime
import settings
import pygame
from random import randrange

f_sine = 0

# Curve 0
# Example for rPolyline function
def square(fwork):

    dots = []

    # "frame" components
    #"""
    x_max = (800) - 1
    y_max = (600) - 1
    #x_max = 1
    #y_max = 1
    x_corner = 20
    y_corner = 15
    dots = [
        (x_corner, y_corner),
        (-x_corner, y_corner),
        (-x_corner, -y_corner),
        (x_corner, -y_corner),
        (x_corner, y_corner)
    ]
    #print dots
    fwork.rPolyLineOneColor (dots, c = colorify.rgb2hex([255, 0, 0]), PL = 0, closed = False, xpos=x_max>>1 , ypos=y_max>>1, resize=1)
    #"""

    # transfer full frame to automatic laser display PL 0 :
    gstt.PL[0] = fwork.LinesPL(0)
    
# Curve 1
def Sine(fwork):
    global f_sine

    dots = []
    amp = 200
    nb_point = 40

    # Laser 0 "frame" components
    for t in range(0, nb_point+1):
        y = 0 - amp*math.sin(2 * PI * (float(t)/float(nb_point)))
        x = 0 - amp*math.cos(2 * PI * f_sine *(float(t)/float(nb_point)))
        dots.append(proj(int(x),int(y),0))
    print dots
    fwork.PolyLineOneColor ( dots, c = colorify.rgb2hex([255,255,0]), PL =  0, closed = False)
    
    # transfer full frame to automatic laser display PL 0 :
    gstt.PL[0] = fwork.LinesPL(0)
    
    if f_sine > 24:
        f_sine = 0
    f_sine += 0.01

# Live 3D rotation and 2D projection for a given 3D point
def proj(x,y,z):

    # Skip trigo update if angleX didn't change 
    # TODO : gstt.prev_cc29 == -1 is useful only the first time to create cosa and sina values

    if gstt.prev_cc29 != gstt.cc[29] or gstt.prev_cc29 == -1: 
        gstt.angleX += cc2range(gstt.cc[29],0,0.1)    
        rad = gstt.angleX * PI / 180
        cosaX = math.cos(rad)
        sinaX = math.sin(rad)
        prev_cc29 = gstt.cc[29]

    y2 = y
    y = y2 * cosaX - z * sinaX
    z = y2 * sinaX + z * cosaX

    # Skip trigo update if angleY didn't change 
    if gstt.prev_cc30 != gstt.cc[30]: 
        gstt.angleY += cc2range(gstt.cc[30],0,0.1)
        rad = gstt.angleY * PI / 180
        cosaY = math.cos(rad)
        sinaY = math.sin(rad)
        prev_cc30 = gstt.cc[30]

    z2 = z
    z = z2 * cosaY - x * sinaY
    x = z2 * sinaY + x * cosaY


    # Skip trigo update if angleZ didn't change 
    if gstt.prev_cc31 != gstt.cc[31]: 
        gstt.angleZ += cc2range(gstt.cc[31],0,0.1)
        rad = gstt.angleZ * PI / 180
        cosZ = math.cos(rad)
        sinZ = math.sin(rad)
        
    x2 = x
    x = x2 * cosZ - y * sinZ
    y = x2 * sinZ + y * cosZ

    # 3D to 2D projection
    factor = 4 * gstt.cc[22] / ((gstt.cc[21] * 8) + z)
    x = x * factor + xy_center [0] 
    y = - y * factor + xy_center [1] 
    
    return x,y

# Remap values in different scales i.e CC value in screen position.
def cc2scrX(s):
    a1, a2 = 0,127  
    b1, b2 = -screen_size[0]/2, screen_size[0]/2
    return  b1 + ((s - a1) * (b2 - b1) / (a2 - a1))

def cc2scrY(s):
    a1, a2 = 0,127  
    b1, b2 = -screen_size[1]/2, screen_size[1]/2
    return  b1 + ((s - a1) * (b2 - b1) / (a2 - a1))

def cc2range(s,min,max):
    a1, a2 = 0,127  
    b1, b2 = min, max
    return  b1 + ((s - a1) * (b2 - b1) / (a2 - a1))

def extracc2scrX(s):
    a1, a2 = -66000,66000  
    b1, b2 = 0, screen_size[0]
    return  b1 + ((s - a1) * (b2 - b1) / (a2 - a1))

def extracc2scrY(s):
    a1, a2 = -66000,66000 
    b1, b2 = 0, screen_size[1]
    return  b1 + ((s - a1) * (b2 - b1) / (a2 - a1))

def extracc2range(s,min,max):
    a1, a2 = -66000,66000  
    b1, b2 = min, max
    return  b1 + ((s - a1) * (b2 - b1) / (a2 - a1))


 