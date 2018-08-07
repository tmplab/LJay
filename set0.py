#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# -*- mode: Python -*-

import math
import gstt
from globalVars import *
import bhorosc
import colorify
import orbits
import numpy as np
import pdb
import time
from jplephem.spk import SPK

kernel = SPK.open('de430.bsp')
gstt.JulianDate = 367 * gstt.year - 7 * (gstt.year + (gstt.month + 9)/12)/4 + 275 * gstt.month/9 + gstt.day + 1721014
print "JD : ", gstt.JulianDate


orbits = orbits.Orbits()
f_sine = 0


# Mode 0
def Sine(fwork):
    global f_sine

    dots = []
    etherlaser = 2
    amp = 200
    nb_point = 40
    for t in range(0, nb_point+1):
        y = 0 - amp*math.sin(2 * PI * (float(t)/float(nb_point)))
        x = 0 - amp*math.cos(2 * PI * f_sine *(float(t)/float(nb_point)))
        dots.append(proj(int(x),int(y),0))

    fwork.PolyLineOneColor ( dots, c = colorify.rgb2hex(gstt.color), PL =  1, closed = False)
    
    gstt.PL[PL] = fwork.LinesPL(PL)
    
    if f_sine > 24:
        f_sine = 0
    f_sine += 0.01

# Curve 1
def xPLS(fwork):
    global f_sine


    # point list "PL" 0 generator (assigned to a laser in gstt.lasersPLS) 
    PL = 0
    dots = []
    
    
    # middle horizontal line
    x = (int(screen_size[1]) / 2) - 50
    y = (int(screen_size[0])/2)
    dots.append((int(x),int(y)))
    dots.append((int((int(screen_size[1]) / 2) + 50),(int(y))))
    
    #gstt.PL[0] = dots
    #gstt.PLcolor[0] = colorify.rgb2hex(gstt.color)
    fwork.PolyLineOneColor(dots, c=colorify.rgb2hex(gstt.color), PL = 0, closed = False)
    
    gstt.PL[PL] = fwork.LinesPL(PL)
   
    
    # PL 1 generator (assigned to a laser in gstt.lasersPLS)
    PL = 1
    dots = []
    
    #pdb.set_trace()
    # middle vertical line
    x = int(screen_size[1]) / 2
    y = (int(screen_size[1])/2) -50
    dots.append((int(x),int(y)))
    dots.append((int(x),(int(screen_size[1])/2)+50))
    
    #gstt.PL[1] = dots
    #gstt.PLcolor[1] = colorify.rgb2hex(gstt.color)
    fwork.PolyLineOneColor(dots, c=colorify.rgb2hex(gstt.color), PL = 1, closed = False)
    
    gstt.PL[PL] = fwork.LinesPL(PL)
    
  
    # PL 2 generator (assigned to a laser in gstt.lasersPLS)
    PL = 2
    dots = []     
    amp = 200
    nb_point = 40
    for t in range(0, nb_point+1):
        y = 0 - amp*math.sin(2 * PI * (float(t)/float(nb_point)))
        x = 0 - amp*math.cos(2 * PI * f_sine *(float(t)/float(nb_point)))
        dots.append(proj(int(x),int(y),0))

    #gstt.PL[PL] = dots
    #gstt.PLcolor[PL] = colorify.rgb2hex(gstt.color)
    
    fwork.PolyLineOneColor ( dots, c = colorify.rgb2hex(gstt.color), PL =  2, closed = False)
    
    gstt.PL[PL] = fwork.LinesPL(PL)
    
    if f_sine > 24:
        f_sine = 0
    f_sine += 0.01


# Curve 2
def Orbits(fwork):

    orbits.Orbits.Draw(fwork)

# Curve 3	
def Dot(fwork):

    dots = []
    x = cc2scrX(gstt.cc[5])
    y = cc2scrY(gstt.cc[6])
    #x = xy_center[0] + gstt.cc[5]*amp    
    #y = xy_center[1] + gstt.cc[6]*amp
    #print x,y,proj(int(x),int(y),0)
    dots.append(proj(int(x),int(y),0))
    dots.append(proj(int(x)+5,int(y)+5,0))
      
    fwork.PolyLineOneColor(dots, c=colorify.rgb2hex(gstt.color))
    gstt.PL[PL] = fwork.LinesPL(PL)

# Curve 4
def Circle(fwork):
    global f_sine

    dots = []
    amp = 200
    nb_point = 40
    for t in range(0, nb_point+1):
        y = 0 - amp*math.sin(2* PI * f_sine *(float(t)/float(nb_point)))
        x = 0 - amp*math.cos(2* PI * f_sine *(float(t)/float(nb_point)))
        dots.append(proj(int(x),int(y),0))

    fwork.PolyLineOneColor( dots, c=colorify.rgb2hex(gstt.color) )
    gstt.PL[PL] = fwork.LinesPL(PL)
    
    #print f_sine
    if f_sine > 24:
        f_sine = 0
    f_sine += 0.01
		

# Curve 5
def CC(fwork):

    dots = []
        
    amp = 200
    nb_point = 60
    for t in range(0, nb_point+1):
        y = 1 - amp*math.sin(2*PI*cc2range(gstt.cc[5],0,24)*(float(t)/float(nb_point)))
        x = 1 - amp*math.cos(2*PI*cc2range(gstt.cc[6],0,24)*(float(t)/float(nb_point))) 
        #bhorosc.send5("/point", [proj(int(x),int(y),0),colorify.rgb2hex(gstt.color)])       
        dots.append(proj(int(x),int(y),0))
        
    fwork.PolyLineOneColor( dots, c=colorify.rgb2hex(gstt.color) )
    gstt.PL[PL] = fwork.LinesPL(PL)


# Curve 6
def Slave(fwork):
    
    fwork.LineTo([gstt.point[0],gstt.point[1]],gstt.point[2])

# Curve 7

def Astro(fwork):

    # PL 0
    #print gstt.JulianDate

    PL = 0
    PlanetsPositions = []
    dots = []
    gstt.PL[PL] = []
    amp = 0.8

    for planet in xrange(9):
        PlanetsPositions.append(kernel[0,planet+1].compute(gstt.JulianDate))

    for planet in xrange(9):

        #print ""
        #print "planet ", planet
        x,y,z = planet2screen(PlanetsPositions[planet][0], PlanetsPositions[planet][1], PlanetsPositions[planet][2])
        #print "x,y,z ", x,y,z
        x,y = proj(int(x),int(y),int(z))
        x = x * amp 
        y = y * amp + 60
        #dots.append((int(x)-300,int(y)+200))
        #dots.append((int(x)-295,int(y)+205))
        fwork.Line((x,y),(x+2,y+2),  c=colorify.rgb2hex(gstt.color), PL=0)
        #fwork.PolyLineOneColor(dots, c=colorify.rgb2hex(gstt.color), PL = 0, closed = False)


    #print dots

    gstt.PL[PL] = fwork.LinesPL(PL)
    #print dots[0][0]

    #print gstt.PL[0]
    #gstt.PLcolor[0] = colorify.rgb2hex(gstt.color)
    
    #time.sleep(0.001)

    gstt.JulianDate +=1

def ssawtooth(samples,freq,phase):

	t = np.linspace(0+phase, 1+phase, samples)
	for ww in range(samples):
		samparray[ww] = signal.sawtooth(2 * np.pi * freq * t[ww])
	return samparray

def ssquare(samples,freq,phase):

	t = np.linspace(0+phase, 1+phase, samples)
	for ww in range(samples):
		samparray[ww] = signal.square(2 * np.pi * freq * t[ww])
	return samparray

def ssine(samples,freq,phase):

	t = np.linspace(0+phase, 1+phase, samples)
	for ww in range(samples):
		samparray[ww] = np.sin(2 * np.pi * freq  * t[ww])
	return samparray


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

def planet2screen(planetx, planety, planetz):
    #screen_size = [800,600]
    a1, a2 = -1e+9,1e+9  
    b1, b2 = 0, screen_size[1]
    x = b1 + ((planetx - a1) * (b2 - b1) / (a2 - a1))
    b1, b2 = 0, screen_size[1]
    y = b1 + ((planety - a1) * (b2 - b1) / (a2 - a1))
    b1, b2 = 0, screen_size[1]
    z = b1 + ((planetz - a1) * (b2 - b1) / (a2 - a1))
    return x,y,z


# 3D rotation and 2D projection for a given 3D point
def proj(x,y,z):

    gstt.angleX += cc2range(gstt.cc[29],0,0.1)
    gstt.angleY += cc2range(gstt.cc[30],0,0.1)
    gstt.angleZ += cc2range(gstt.cc[31],0,0.1)
    
    rad = gstt.angleX * PI / 180
    cosa = math.cos(rad)
    sina = math.sin(rad)
    y2 = y
    y = y2 * cosa - z * sina
    z = y2 * sina + z * cosa

    rad = gstt.angleY * PI / 180
    cosa = math.cos(rad)
    sina = math.sin(rad)
    z2 = z
    z = z2 * cosa - x * sina
    x = z2 * sina + x * cosa

    rad = gstt.angleZ * PI / 180
    cosa = math.cos(rad)
    sina = math.sin(rad)
    x2 = x
    x = x2 * cosa - y * sina
    y = x2 * sina + y * cosa

    # 3D to 2D projection
    factor = 4 * gstt.cc[22] / ((gstt.cc[21] * 8) + z)
    x = x * factor + xy_center [0] 
    y = - y * factor + xy_center [1] 

    return x,y

