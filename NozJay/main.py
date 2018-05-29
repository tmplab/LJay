#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# -*- mode: Python -*-

'''
Main test (Emvivre)

Inspired from Empty Laser (Sam Neurohack) 
LICENCE : CC
'''

import pygame
import math
import random
import itertools
import sys
import os
import thread
import time
import frame
import renderer
import dac
from globalVars import *

import bhorosc
import orbits
import midi
import gstt
import sv
import colorify

import collections

if not gstt.SLAVERY :
	midi.InConfig()
	midi.OutConfig()
	#import nozoid
	
orbits = orbits.Orbits()
f_sine = 0
x = 0

dotsosc = collections.deque(maxlen=10)
dotsosc0 = collections.deque(maxlen=10)
dotsosc1 = collections.deque(maxlen=10)
currentdotsosc=0

#dots = []

if gstt.debug == 0:
	print "NO DEBUG"

print "Starting Laser..."

def dac_thread():
	while True:
		try:
			d = dac.DAC(dac.find_first_dac())
			d.play_stream(laser)
		except Exception as e:

			import sys, traceback
			if gstt.debug == 2:
				print '\n---------------------'
				print 'Exception: %s' % e
				print '- - - - - - - - - - -'
				traceback.print_tb(sys.exc_info()[2])
				print "\n"
			pass

def DrawTestPattern(f):
	l,h = screen_size
	L_SLOPE = 30
	
	f.Line((0, 0), (l, 0), 0xFFFFFF)
	f.LineTo((l, h), 0xFFFFFF)
	f.LineTo((0, h), 0xFFFFFF)
	f.LineTo((0, 0), 0xFFFFFF)
	
	f.LineTo((2*L_SLOPE, h), 0)
	for i in xrange(1,7):
		c = (0xFF0000 if i & 1 else 0) | (0xFF00 if i & 2 else 0) | (0xFF if i & 4 else 0)
		f.LineTo(((2 * i + 1) * L_SLOPE, 0), c)
		f.LineTo(((2 * i + 2) * L_SLOPE, h), c)
	f.Line((l*.5, h*.5), (l*.75, -h*.5), 0xFF00FF)
	f.LineTo((l*1.5, h*.5), 0xFF00FF)
	f.LineTo((l*.75, h*1.5), 0xFF00FF)
	f.LineTo((l*.5, h*.5), 0xFF00FF)

def Align(f):
	l,h = screen_size
	L_SLOPE = 30
	
	f.Line((0, 0), (l, 0), 0xFFFFFF)
	f.LineTo((l, h), 0xFFFFFF)
	f.LineTo((0, h), 0xFFFFFF)
	f.LineTo((0, 0), 0xFFFFFF)
	laser = renderer.LaserRenderer(fwork_holder, gstt.centerx, gstt.centery, gstt.zoomx, gstt.zoomy, gstt.sizex, gstt.sizey)

	print str(gstt.centerx) + "," + str(gstt.centery) + "," + str(gstt.zoomx) + "," + str(gstt.zoomy) + "," + str(gstt.sizex) + "," + str(gstt.sizey)



def alignjump():
	
	if keystates[pygame.K_p]:
		DrawTestPattern(fwork)
		
	if keystates[pygame.K_x]:
		Align(fwork)
		
	if keystates[pygame.K_r]:
		gstt.centerx += 20
		Align(fwork)

	if keystates[pygame.K_t]:
		gstt.centerx -= 20
		Align(fwork)
		
	if keystates[pygame.K_y]:
		gstt.centery += 20
		Align(fwork)

	if keystates[pygame.K_u]:
		gstt.centery -= 20
		Align(fwork)

	if keystates[pygame.K_f]:
		gstt.zoomx += 0.1
		Align(fwork)

	if keystates[pygame.K_g]:
		gstt.zoomx -= 0.1
		Align(fwork)
		
	if keystates[pygame.K_h]:
		gstt.zoomy += 0.1
		Align(fwork)

	if keystates[pygame.K_j]:
		gstt.zoomy -= 0.1
		Align(fwork)
	
	if keystates[pygame.K_c]:
		gstt.sizex -= 50
		Align(fwork)
		
	if keystates[pygame.K_v]:
		gstt.sizex += 50
		Align(fwork)
		
	if keystates[pygame.K_b]:
		gstt.sizey -= 50
		Align(fwork)
		
	if keystates[pygame.K_n]:
		gstt.sizey += 50
		Align(fwork)
		
	if keystates[pygame.K_l]:
		gstt.finangle -= 0.001
		Align(fwork)
		
	if keystates[pygame.K_m]:
		gstt.finangle += 0.001
		Align(fwork)


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

# Mode 0
def NozMode():
    global f_sine,x
    global dotsosc
    global dotsosc0
    global dotsosc1
    global currentdotsosc
    #global dots
    #dots = []
        
    amp = 200
    nb_point = 40
    nbplow=10
    nbphigh=50
    '''
    for t in range(0, nb_point+1):
    
        #y = cc2scrX((66000 + gstt.osc[4])%127)
        #x = cc2scrX((66000 + gstt.osc[5])%127)
        #rint x,y
    	x = 3.5 *(extracc2scrX(gstt.osc[gstt.X]) - 400)
    	y = 3.5 *(extracc2scrY(gstt.osc[gstt.Y]) - 300)
        #print proj(int(x),int(y),0)
        dots.append(proj(int(x),int(y),0))
        
    fwork.PolyLineOneColor( dots, c=colorify.rgb2hex(gstt.color)  )
    '''
    #x = cc2scrX((66000 + gstt.osc[4])%127)
    #x += 1
    #if x >= 840:
    #    x = -840

    #read lfo # or osc #
    #x = 1.8 *(extracc2scrX(gstt.osc[1]) - 300)

    #x = 1.8 *(extracc2scrX(gstt.osc[gstt.X]) - 400) 
    #print gstt.OscXY[0]
    #print gstt.OscXY[1]
    #print gstt.OscXY[2]

    if gstt.X != 0:
	#print "gstt.X != 0 (== %d)" % gstt.X
	if (dotsosc.maxlen == nbphigh and gstt.Y != 0):
		print "X changing size of dotsocs (%d) to %d"%(dotsosc.maxlen,nbplow)
		dotsosc = collections.deque(maxlen=nbplow)
	xT = gstt.osc[gstt.X]
        x = 3.5 * (extracc2scrX(xT) - 400)
    else:
	#print "gstt.X == 0"
	if (gstt.Y != 0 and dotsosc.maxlen == nbplow):
		print "X changing size of dotsocs (%d) to %d"%(dotsosc.maxlen,nbphigh)
		dotsosc = collections.deque(maxlen=nbphigh)
	xT = (((time.time()*50000) % 65536) - 32768)
	x = 3.5 * (extracc2scrX(xT) - 400)
	#print "x:%r,xT:%r" % (x,xT)

    #x = 3.5 * (extracc2scrX(xT) - 400)
    #x = 3.5 *(extracc2scrX(gstt.osc[gstt.X]) - 400)
    #y = cc2scrX((32000 + gstt.osc[4])%127)
    #y = 3 *(extracc2scrY(gstt.osc[2]) - 300)

    if gstt.Y != 0:
	#print "gstt.Y != 0 (== %d)" % gstt.Y
	if (dotsosc.maxlen == nbphigh and gstt.X != 0):
		print "Y changing size of dotsocs (%d) to %d"%(dotsosc.maxlen,nbplow)
		dotsosc = collections.deque(maxlen=nbplow)
	yT = gstt.osc[gstt.Y]
    	y = 3.5 * (extracc2scrY(yT) - 300)
    else:
	#print "gstt.Y == 0"
	if (gstt.X != 0 and dotsosc.maxlen == nbplow):
		print "Y changing size of dotsocs (%d) to %d"%(dotsosc.maxlen,nbphigh)
		dotsosc = collections.deque(maxlen=nbphigh)
	yT = (((time.time()*50000) % 65536) - 32768)
    	y = 3.5 * (extracc2scrY(yT) - 300)
	#print "y:%r,yT:%r" % (y,yT)

    if gstt.X == 0 and gstt.Y == 0:
	x = 0
	y = 0

    #y = 3.5 * (extracc2scrY(yT) - 300)
    #y = 3.5 *(extracc2scrY(gstt.osc[gstt.Y]) - 300)
    #print x,y
    #gstt.cc[22]=extracc2range(gstt.osc[6],0,127)
    newx,newy =  proj(int(x),int(y),0)
    #print "NX: %r, NY: %r" % (newx,newy)
    #dots.append(proj(int(x),int(y),0))    
    #if len(dots) >= 5:
    #	dots = []
    #newxR=newx+random.randint(-200,200)
    #newyR=newy+random.randint(-100,100)
    #dots.append((newx+random.randint(-200,200),newy+random.randint(-100,100)))
    #dotsosc.append((newx+random.randint(-200,200),newy+random.randint(-100,100)))
    #dots.append((newxR,newyR))
    #dotsosc.append((newxR,newyR))

    #if gstt.X == 0 and gstt.Y != 0:
	#lastP=dotsosc[-1]
    	#if (newx < lastP[0]):
	#	currentdotsosc=(currentdotsosc+1)%2
	#	print "Switching dotosc to #%d"%currentdotsosc
		

    dotsosc.append((newx,newy))

#    if currentdotosc == 0:
#	if newx >= dotosc0

#    dotsosc0.append((newx,newy))
#    dotsosc1.append((newx,newy))

    #print dots
    #print dotsosc
    #print "LastP X",type(dotsosc[-1][0])
    #print "LastP Y",dotsosc[-1][1]
    
    #fwork.Line((newx,newy),(newx+ 5,newy+5), colorify.rgb2hex(gstt.color) )



    #fwork.PolyLineOneColor( dots, c=colorify.rgb2hex(gstt.color)  )

    fwork.PolyLineOneColor( dotsosc, c=colorify.rgb2hex(gstt.color)  )

#    fwork.PolyLineOneColor( dotsosc0, c=colorify.rgb2hex(gstt.color)  )
#    fwork.PolyLineOneColor( dotsosc1, c=colorify.rgb2hex(gstt.color)  )

    #fwork.PolyLineOneColor( reversed(dotsosc), c=colorify.rgb2hex(gstt.color)  )
    #fwork.Line((newx,newy),(newx+ 1,newy+1), colorify.rgb2hex(gstt.color) )
    fwork.Line((newx,10),(newx+ 1,10+1), colorify.rgb2hex(gstt.color) )
    fwork.Line((10,newy),(10,newy+1), colorify.rgb2hex(gstt.color) )
    #time.sleep(0.1)

# Mode 1
def SineMode():
    global f_sine

    dots = []
        
    amp = 200
    nb_point = 40
    for t in range(0, nb_point+1):
        y = 0 - amp*math.sin(2 * PI * (float(t)/float(nb_point)))
        x = 0 - amp*math.cos(2 * PI * f_sine *(float(t)/float(nb_point)))
        dots.append(proj(int(x),int(y),0))

    fwork.PolyLineOneColor( dots, c=colorify.rgb2hex(gstt.color)  )
    
    if f_sine > 24:
        f_sine = 0
    f_sine += 0.01

# Mode 2
def OrbitsMode():

    orbits.Draw(fwork)


# Mode 3	
def DotMode():

    dots = []
    x = cc2scrX(gstt.cc[1])
    y = cc2scrY(gstt.cc[2])
    #x = xy_center[0] + gstt.cc[1]*amp    
    #y = xy_center[1] + gstt.cc[2]*amp
    print x,y,proj(int(x),int(y),0)
    dots.append(proj(int(x),int(y),0))
    dots.append(proj(int(x)+5,int(y)+5,0))
    
    fwork.PolyLineOneColor(dots, c=colorify.rgb2hex(gstt.color)  )

# Mode 4
def CircleMode():
    global f_sine

    dots = []
    amp = 200
    nb_point = 40
    for t in range(0, nb_point+1):
        y = 0 - amp*math.sin(2* PI * f_sine *(float(t)/float(nb_point)))
        x = 0 - amp*math.cos(2* PI * f_sine *(float(t)/float(nb_point)))
        dots.append(proj(int(x),int(y),0))

    fwork.PolyLineOneColor( dots, c=colorify.rgb2hex(gstt.color) )
    
    print f_sine
    if f_sine > 24:
        f_sine = 0
    f_sine += 0.01
		

# Mode 5
def CCMode():

    dots = []
        
    amp = 200
    nb_point = 60
    for t in range(0, nb_point+1):
        y = 1 - amp*math.sin(2*PI*cc2range(gstt.cc[5],0,24)*(float(t)/float(nb_point)))
        x = 1 - amp*math.cos(2*PI*cc2range(gstt.cc[6],0,24)*(float(t)/float(nb_point))) 
        bhorosc.send5("/point", [proj(int(x),int(y),0),colorify.rgb2hex(gstt.color)])       
        dots.append(proj(int(x),int(y),0))
        
    fwork.PolyLineOneColor( dots, c=colorify.rgb2hex(gstt.color) )



# Mode 6
def SlaveMode():
    
    fwork.LineTo([gstt.point[0],gstt.point[1]],gstt.point[2])


# Mode 7
def NozMode2():
    global f_sine,x
    global dotsosc
    global dotsosc0
    global dotsosc1
    global currentdotsosc
    #global dots
    #dots = []
        
    amp = 200
    nb_point = 40
    nbplow=10
    nbphigh=50
    '''
    for t in range(0, nb_point+1):
    
        #y = cc2scrX((66000 + gstt.osc[4])%127)
        #x = cc2scrX((66000 + gstt.osc[5])%127)
        #rint x,y
    	x = 3.5 *(extracc2scrX(gstt.osc[gstt.X]) - 400)
    	y = 3.5 *(extracc2scrY(gstt.osc[gstt.Y]) - 300)
        #print proj(int(x),int(y),0)
        dots.append(proj(int(x),int(y),0))
        
    fwork.PolyLineOneColor( dots, c=colorify.rgb2hex(gstt.color)  )
    '''
    #x = cc2scrX((66000 + gstt.osc[4])%127)
    #x += 1
    #if x >= 840:
    #    x = -840

    #read lfo # or osc #
    #x = 1.8 *(extracc2scrX(gstt.osc[1]) - 300)

    #x = 1.8 *(extracc2scrX(gstt.osc[gstt.X]) - 400) 
    #print gstt.OscXY[0]
    #print gstt.OscXY[1]
    #print gstt.OscXY[2]

    if gstt.X != 0:
	#print "gstt.X != 0 (== %d)" % gstt.X
	if (dotsosc.maxlen == nbphigh and gstt.Y != 0):
		print "X changing size of dotsocs (%d) to %d"%(dotsosc.maxlen,nbplow)
		dotsosc = collections.deque(maxlen=nbplow)
	xT = gstt.osc[gstt.X]
        x = 3.5 * (extracc2scrX(xT) - 400)
    else:
	#print "gstt.X == 0"
	if (gstt.Y != 0 and dotsosc.maxlen == nbplow):
		print "X changing size of dotsocs (%d) to %d"%(dotsosc.maxlen,nbphigh)
		dotsosc = collections.deque(maxlen=nbphigh)
	xT = (((time.time()*50000) % 65536) - 32768)
	x = 3.5 * (extracc2scrX(xT) - 400)
	#print "x:%r,xT:%r" % (x,xT)

    #x = 3.5 * (extracc2scrX(xT) - 400)
    #x = 3.5 *(extracc2scrX(gstt.osc[gstt.X]) - 400)
    #y = cc2scrX((32000 + gstt.osc[4])%127)
    #y = 3 *(extracc2scrY(gstt.osc[2]) - 300)

    if gstt.Y != 0:
	#print "gstt.Y != 0 (== %d)" % gstt.Y
	if (dotsosc.maxlen == nbphigh and gstt.X != 0):
		print "Y changing size of dotsocs (%d) to %d"%(dotsosc.maxlen,nbplow)
		dotsosc = collections.deque(maxlen=nbplow)
	yT = gstt.osc[gstt.Y]
    	y = 3.5 * (extracc2scrY(yT) - 300)
    else:
	#print "gstt.Y == 0"
	if (gstt.X != 0 and dotsosc.maxlen == nbplow):
		print "Y changing size of dotsocs (%d) to %d"%(dotsosc.maxlen,nbphigh)
		dotsosc = collections.deque(maxlen=nbphigh)
	yT = (((time.time()*50000) % 65536) - 32768)
    	y = 3.5 * (extracc2scrY(yT) - 300)
	#print "y:%r,yT:%r" % (y,yT)

    if gstt.X == 0 and gstt.Y == 0:
	x = 0
	y = 0

    #y = 3.5 * (extracc2scrY(yT) - 300)
    #y = 3.5 *(extracc2scrY(gstt.osc[gstt.Y]) - 300)
    #print x,y
    #gstt.cc[22]=extracc2range(gstt.osc[6],0,127)

    newx,newy =  proj(int(x),int(y),0)

    #print "NX: %r, NY: %r" % (newx,newy)
    #dots.append(proj(int(x),int(y),0))    
    #if len(dots) >= 5:
    #	dots = []
    #newxR=newx+random.randint(-200,200)
    #newyR=newy+random.randint(-100,100)
    #dots.append((newx+random.randint(-200,200),newy+random.randint(-100,100)))
    #dotsosc.append((newx+random.randint(-200,200),newy+random.randint(-100,100)))
    #dots.append((newxR,newyR))
    #dotsosc.append((newxR,newyR))

    dotsosc.append((newx,newy))

#    if currentdotosc == 0:
#	if newx >= dotosc0

#    dotsosc0.append((newx,newy))
#    dotsosc1.append((newx,newy))

    #print dots
    #print dotsosc
    
    #fwork.Line((newx,newy),(newx+ 5,newy+5), colorify.rgb2hex(gstt.color) )



    #fwork.PolyLineOneColor( dots, c=colorify.rgb2hex(gstt.color)  )

    fwork.PolyLineOneColor( dotsosc, c=colorify.rgb2hex(gstt.color)  )

#    fwork.PolyLineOneColor( dotsosc0, c=colorify.rgb2hex(gstt.color)  )
#    fwork.PolyLineOneColor( dotsosc1, c=colorify.rgb2hex(gstt.color)  )

    #fwork.PolyLineOneColor( reversed(dotsosc), c=colorify.rgb2hex(gstt.color)  )
    #fwork.Line((newx,newy),(newx+ 1,newy+1), colorify.rgb2hex(gstt.color) )
#    fwork.Line((newx,10),(newx+ 1,10+1), colorify.rgb2hex(gstt.color) )
#    fwork.Line((10,newy),(10,newy+1), colorify.rgb2hex(gstt.color) )
    #time.sleep(0.1)


# Inits

app_path = os.path.dirname(os.path.realpath(__file__))

pygame.init()
screen = pygame.display.set_mode(screen_size)
if gstt.SLAVERY == False:
	pygame.display.set_caption("Laser Master")
else:
	pygame.display.set_caption("Laser Slave ",str(gstt.SLAVERY))

clock = pygame.time.Clock()


fwork_holder = frame.FrameHolder()
laser = renderer.LaserRenderer(fwork_holder, gstt.centerx, gstt.centery, gstt.zoomx, gstt.zoomy, gstt.sizex, gstt.sizey)
thread.start_new_thread(dac_thread, ())

update_screen = False
keystates = pygame.key.get_pressed()
(SCREEN_W, SCREEN_H) = screen_size


jumptable =  {
        0: NozMode,
        1: SineMode,
        2: OrbitsMode,
        3: DotMode,
        4: CircleMode,
        5: CCMode,
        6: SlaveMode,
        7: NozMode2
    }

print ""
if gstt.SLAVERY != False:
	print "Node Slavery Mode : ", str(gstt.SLAVERY)
else: 
	print "Node Mode : MASTER"


# Main loop

while True:

    # Pygame 
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			break

	keystates_prev = keystates[:]
	keystates = pygame.key.get_pressed()[:]

        if keystates[pygame.K_ESCAPE]:
                break
        	
	screen.fill(0)
	fwork = frame.Frame()
	
	# align mode ?
	alignjump()

	# Colorify
	colorify.jump()

	# Points generation
	
	doit = jumptable.get(gstt.Mode)
	doit()

	# pending osc message ?
	bhorosc.osc_frame()


	fwork_holder.f = fwork

	if update_screen:
		update_screen = False
		fwork.RenderScreen(screen)
		pygame.display.flip()
	else:
		update_screen = True
	clock.tick(100)

pygame.quit()
