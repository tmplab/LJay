#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# -*- mode: Python -*-

'''
Laser Jaying

LICENCE : CC
'''
#from __future__ import print_function 
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
import newdac
#import dac2
import ConfigParser
from globalVars import *

import gstt
import cli
import colorify
import pdb

print ""
print "LJay"
print ""
print "Autoconfiguring..."


def WriteSettings(): 


	config.set('General', 'set', str(gstt.Set))
	config.set('General', 'curve', str(gstt.Curve))
	config.set('General', 'lasernumber', str(gstt.LaserNumber))

	# Multilaser style
	for i in range(gstt.LaserNumber):
		laser = 'laser' + str(i)
		config.set
		config.set(laser, 'centerx', str(gstt.centerX[i]))
		config.set(laser, 'centery', str(gstt.centerY[i]))
		config.set(laser, 'zoomx', str(gstt.zoomX[i]))
		config.set(laser, 'zoomy', str(gstt.zoomY[i]))
		config.set(laser, 'sizex', str(gstt.sizeX[i]))
		config.set(laser, 'sizey', str(gstt.sizeY[i]))
		config.set(laser, 'finangle', str(gstt.finANGLE[i]))
		config.set(laser, 'swapx', str(gstt.swapX[i]))
		config.set(laser, 'swapy', str(gstt.swapY[i]))

	# Legacy mono laser style
	config.set('laser1', 'centerx', str(gstt.centerx))
	config.set('laser1', 'centery', str(gstt.centery))
	config.set('laser1', 'zoomx', str(gstt.zoomx))
	config.set('laser1', 'zoomy', str(gstt.zoomy))
	config.set('laser1', 'sizex', str(gstt.sizex))
	config.set('laser1', 'sizey', str(gstt.sizey))
	config.set('laser1', 'finangle', str(gstt.finangle))
	config.set('laser1', 'swapx', str(gstt.swapx))
	config.set('laser1', 'swapy', str(gstt.swapy))


	config.write(open('settings.conf','w'))



def ReadSettings(): 
	

	gstt.Set = config.getint('General', 'set')
	gstt.Curve = config.getint('General', 'curve')
	gstt.LaserNumber = config.getint('General', 'lasernumber')

	# Legacy mono laser style
	#gstt.color = config.getint('laser1', 'color')
	gstt.centerx = config.getint('laser1', 'centerx')
	gstt.centery = config.getint('laser1', 'centery')
	gstt.zoomx = config.getfloat('laser1', 'zoomx')
	gstt.zoomy = config.getfloat('laser1', 'zoomy')
	gstt.sizex = config.getint('laser1', 'sizex')
	gstt.sizey = config.getint('laser1', 'sizey')
	gstt.finangle = config.getfloat('laser1', 'finangle')
	gstt.swapx = config.getint('laser1', 'swapx')
	gstt.swapy = config.getint('laser1', 'swapy')
	
	# Multilaser style
	for i in range(4):
		laser = 'laser' + str(i)
		gstt.lasersIPS[i]= config.get(laser, 'ip')
		gstt.lasersPLS[i] = config.getint(laser, 'PL')
		#gstt.lasersPLcolor[i] = config.getint(laser, 'color')
		gstt.centerX[i]= config.getint(laser, 'centerx')
		gstt.centerY[i] = config.getint(laser, 'centery')
		gstt.zoomX[i] = config.getfloat(laser, 'zoomx')
		gstt.zoomY[i] = config.getfloat(laser, 'zoomy')
		gstt.sizeX[i] = config.getint(laser, 'sizex')
		gstt.sizeY[i] = config.getint(laser, 'sizey')
		gstt.finANGLE[i] = config.getfloat(laser, 'finangle')
		gstt.swapX[i] = config.getint(laser, 'swapx')
		gstt.swapY[i] = config.getint(laser, 'swapy')


config = ConfigParser.ConfigParser()
config.read("settings.conf")



ReadSettings()

print ""
print "Set : ", gstt.Set
print "Curve : ", gstt.Curve
print "Lasers number : ", gstt.LaserNumber
print ""
print "Lasers parameters..."
print "IPs ", gstt.lasersIPS
print "PLs : ", gstt.lasersPLS
#print "Colors TODO : ", gstt.lasersPLcolor
print "center X : ", gstt.centerX
print "center Y : ",gstt.centerY
print "zoom X : ", gstt.zoomX
print "zoom Y : ", gstt.zoomY
print "size X : ", gstt.sizeX
print "size Y : ", gstt.sizeY
print "Rotation : ", gstt.finANGLE
print "swap X : ", gstt.swapX
print "swap Y : ", gstt.swapY


cli.handle()

WriteSettings()

#raw_input("Hit Enter To Continue!")

import midi
import bhorosc
import set0
import set1
import setllstr
import orbits

if not gstt.SLAVERY :
	midi.InConfig()
	midi.OutConfig()

#dots = []

x = 0

settables =  {					# Set 0
        0: set0.Sine,
        1: set0.xPLS,
        2: set0.Orbits,
        3: set0.Dot,
        4: set0.Circle,
        5: set0.CC,
        6: set0.Orbits,
        7: set0.Astro
    }, {						# Set 1
        0: set1.LineX,
        1: set1.Sine,
        2: set1.Orbits,
        3: set1.Dot,
        4: set1.Circle,
        5: set1.CC,
        6: set1.Slave
    }, {						# setllstr
        0: setllstr.NozMode,
        1: setllstr.NozMode2,
        2: setllstr.Sine,
        3: setllstr.Orbits,
        4: setllstr.Circle,
        5: setllstr.CC,
        6: setllstr.Slave
    }


if gstt.debug == 0:
	print "NO DEBUG"

'''
def dac_thread():
	while True:
		try:
			d = dac.DAC(etherIP)
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

def dac_thread0():
    while True:
        try:
            d0 = dac2.DAC(gstt.lasersIPS[0],gstt.lasersPLS[0])
            d0.play_stream()
        except Exception as e:

            import sys, traceback
            if gstt.debug == 2:
                print '\n---------------------'
                print 'Exception: %s' % e
                print '- - - - - - - - - - -'
                traceback.print_tb(sys.exc_info()[2])
                print "\n"
            pass
'''        
def dac_thread0():
    while True:
        try:
            d0 = newdac.DAC(gstt.lasersIPS[0],gstt.lasersPLS[0])
            d0.play_stream()
        except Exception as e:

            import sys, traceback
            if gstt.debug == 2:
                print '\n---------------------'
                print 'Exception: %s' % e
                print '- - - - - - - - - - -'
                traceback.print_tb(sys.exc_info()[2])
                print "\n"
            pass
'''
def dac_thread0():
    while True:
        try:
            d0 = dac.DAC(gstt.lasersIPS[0],gstt.lasersPLS[0])
            d0.play_stream(laser)
        except Exception as e:

            import sys, traceback
            if gstt.debug == 2:
                print '\n---------------------'
                print 'Exception: %s' % e
                print '- - - - - - - - - - -'
                traceback.print_tb(sys.exc_info()[2])
                print "\n"
            pass

'''
def dac_thread1():
    while True:
        try:

            d1 = newdac.DAC(gstt.lasersIPS[1],gstt.lasersPLS[1])
            d1.play_stream()

            # Legacy style
            #d1 = dac.DAC(gstt.lasersIPS[1],gstt.lasersPLS[1])
            #d1.play_stream(laser)
        except Exception as e:

            import sys, traceback
            if gstt.debug == 2:
                print '\n---------------------'
                print 'Exception: %s' % e
                print '- - - - - - - - - - -'
                traceback.print_tb(sys.exc_info()[2])
                print "\n"
            pass


def dac_thread2():
    while True:
        try:
            d2 = newdac.DAC(gstt.lasersIPS[2],gstt.lasersPLS[2])
            d2.play_stream()
        except Exception as e:

            import sys, traceback
            if gstt.debug == 2:
                print '\n---------------------'
                print 'Exception: %s' % e
                print '- - - - - - - - - - -'
                traceback.print_tb(sys.exc_info()[2])
                print "\n"
            pass


def dac_thread3():
    while True:
        try:
            d3 = dac.DAC(gstt.lasersIPS[3],gstt.lasersPLS[3])
            d3.play_stream(laser)
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
	
	f.Line((0, 0), (l, 0), 0xFFFFFF, gstt.simuPL)
	f.LineTo((l, h), 0xFFFFFF, gstt.simuPL)
	f.LineTo((0, h), 0xFFFFFF, gstt.simuPL)
	f.LineTo((0, 0), 0xFFFFFF, gstt.simuPL)
	
	f.LineTo((2*L_SLOPE, h), 0, gstt.simuPL)
	for i in xrange(1,7):
		c = (0xFF0000 if i & 1 else 0) | (0xFF00 if i & 2 else 0) | (0xFF if i & 4 else 0)
		f.LineTo(((2 * i + 1) * L_SLOPE, 0), c, gstt.simuPL)
		f.LineTo(((2 * i + 2) * L_SLOPE, h), c, gstt.simuPL)
	f.Line((l*.5, h*.5), (l*.75, -h*.5), 0xFF00FF, gstt.simuPL)
	f.LineTo((l*1.5, h*.5), 0xFF00FF, gstt.simuPL)
	f.LineTo((l*.75, h*1.5), 0xFF00FF, gstt.simuPL)
	f.LineTo((l*.5, h*.5), 0xFF00FF, gstt.simuPL)

def Align(f):
	l,h = screen_size
	L_SLOPE = 30
	
	f.Line((0, 0), (l, 0), 0xFFFFFF, gstt.simuPL)
	f.LineTo((l, h), 0xFFFFFF, gstt.simuPL)
	f.LineTo((0, h), 0xFFFFFF, gstt.simuPL)
	f.LineTo((0, 0), 0xFFFFFF, gstt.simuPL)

	laser = renderer.LaserRenderer(fwork_holder, gstt.centerx, gstt.centery, gstt.zoomx, gstt.zoomy, gstt.sizex, gstt.sizey)

	WriteSettings()
	print str(gstt.centerx) + "," + str(gstt.centery) + "," + str(gstt.zoomx) + "," + str(gstt.zoomy) + "," + str(gstt.sizex) + "," + str(gstt.sizey)



def alignjump():
	
	if keystates[pygame.K_p]:
		DrawTestPattern(fwork)
		
	if keystates[pygame.K_x]:
		Align(fwork)
		
	if keystates[pygame.K_r]:
		gstt.centerx -= 20
		Align(fwork)

	if keystates[pygame.K_t]:
		gstt.centerx += 20
		Align(fwork)
		
	if keystates[pygame.K_y]:
		gstt.centery -= 20
		Align(fwork)

	if keystates[pygame.K_u]:
		gstt.centery += 20
		Align(fwork)

	if keystates[pygame.K_f]:
		gstt.zoomx -= 0.1
		Align(fwork)

	if keystates[pygame.K_g]:
		gstt.zoomx += 0.1
		Align(fwork)
		
	if keystates[pygame.K_h]:
		gstt.zoomy -= 0.1
		Align(fwork)

	if keystates[pygame.K_j]:
		gstt.zoomy += 0.1
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



# Inits

app_path = os.path.dirname(os.path.realpath(__file__))

pygame.init()
screen = pygame.display.set_mode(screen_size)


if gstt.SLAVERY == False:

	pygame.display.set_caption("Laser Master")
	
	print ""
	gstt.Nbpads = pygame.joystick.get_count()
	print "Joypads : ", str(gstt.Nbpads)

	if gstt.Nbpads > 1:

		gstt.pad2 = pygame.joystick.Joystick(1)
		gstt.pad2.init()

		print gstt.pad2.get_name()
		print "Axis : ", str(gstt.pad2.get_numaxes())
		numButtons = gstt.pad2.get_numbuttons()
		print "Buttons : " , str(numButtons)

	if gstt.Nbpads > 0:

		gstt.pad1 = pygame.joystick.Joystick(0)
		gstt.pad1.init()

		print gstt.pad1.get_name()


		print "Axis : ", str(gstt.pad1.get_numaxes())
		numButtons = gstt.pad1.get_numbuttons()
		print "Buttons : " , str(numButtons)


	
else:
	pygame.display.set_caption("Laser Slave ",str(gstt.SLAVERY))

clock = pygame.time.Clock()


fwork_holder = frame.FrameHolder()
laser = renderer.LaserRenderer(fwork_holder, gstt.centerx, gstt.centery, gstt.zoomx, gstt.zoomy, gstt.sizex, gstt.sizey)


print ""
print "Settings require", gstt.LaserNumber, "lasers." 

'''
print os.system("ping -c 1 " + gstt.lasersIPS[0])
for lasercheck in xrange(gstt.LaserNumber):
	if os.system("ping -c 1 " + gstt.lasersIPS[lasercheck]) == 256:
		print gstt.lasersIPS[lasercheck], "IS NOT CONNECTED"
'''

#thread.start_new_thread(dac_thread, ())

thread.start_new_thread(dac_thread0, ())
print ""
print "dac thread 0 with IP : ", gstt.lasersIPS[0]," and point list : ", gstt.lasersPLS[0],


thread.start_new_thread(dac_thread1, ())
print ""
print "dac thread 1 with IP : ", gstt.lasersIPS[1]," and point list : ", gstt.lasersPLS[1],

'''
thread.start_new_thread(dac_thread2, ())
print ""
print "dac thread 2 with IP : ", gstt.lasersIPS[2]," and point list : ", gstt.lasersPLS[2],

thread.start_new_thread(dac_thread3, ())
print ""
print "dac thread 2 with IP : ", gstt.lasersIPS[3]," and point list : ", gstt.lasersPLS[3],

'''

update_screen = False
keystates = pygame.key.get_pressed()
(SCREEN_W, SCREEN_H) = screen_size


gstt.jumptable = settables[gstt.Set]


print ""
if gstt.SLAVERY != False:
	print "Node Slavery Mode : ", str(gstt.SLAVERY)
else: 
	print "Node Mode : MASTER"
print "Simulator displays point list : ", str(gstt.simuPL)


WriteSettings()

print ""
print "Starting Laser..."

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
	
	doit = gstt.jumptable.get(gstt.Curve)
	doit(fwork)

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
	time.sleep(0.0001)

pygame.quit()




