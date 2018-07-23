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
import ConfigParser
from globalVars import *

import gstt
import colorify

import argparse

print ""
print "LJay"
print ""
print "Autoconfiguring..."

def WriteSettings(): 

	config.set('laser1', 'centerx', str(gstt.centerx))
	config.set('laser1', 'centery', str(gstt.centery))
	config.set('laser1', 'zoomx', str(gstt.zoomx))
	config.set('laser1', 'zoomy', str(gstt.zoomy))
	config.set('laser1', 'sizex', str(gstt.sizex))
	config.set('laser1', 'sizey', str(gstt.sizey))
	config.set('laser1', 'finangle', str(gstt.finangle))
	config.set('laser1', 'swapx', str(gstt.swapx))
	config.set('laser1', 'swapy', str(gstt.swapy))
	config.set('laser1', 'set', str(gstt.Set))
	config.set('laser1', 'curve', str(gstt.Curve))
	config.write(open('settings.conf','w'))

def ReadSettings(): 
	
	gstt.centerx = config.getint('laser1', 'centerx')
	gstt.centery = config.getint('laser1', 'centery')
	gstt.zoomx = config.getfloat('laser1', 'zoomx')
	gstt.zoomy = config.getfloat('laser1', 'zoomy')
	gstt.sizex = config.getint('laser1', 'sizex')
	gstt.sizey = config.getint('laser1', 'sizey')
	gstt.finangle = config.getfloat('laser1', 'finangle')
	gstt.swapx = config.getint('laser1', 'swapx')
	gstt.swapy = config.getint('laser1', 'swapy')
	gstt.Set = config.getint('laser1', 'set')
	gstt.Curve = config.getint('laser1', 'curve')



config = ConfigParser.ConfigParser()
config.read("settings.conf")

ReadSettings()

print ""
print "Arguments parsing if needed..."
#have to be done before importing bhorosc.py to get correct port assignment
argsparser = argparse.ArgumentParser(description="LJay")
argsparser.add_argument("-i","--iport",help="OSC port number to listen to (8001 by default)",type=int)
argsparser.add_argument("-o","--oport",help="OSC port number to send to (8002 by default)",type=int)
argsparser.add_argument("-x","--invx",help="Invert X axis",action="store_true")
argsparser.add_argument("-y","--invy",help="Invert Y axis",action="store_true")
argsparser.add_argument("-s","--set",help="Specify wich generator set to use (default is in gstt.py)",type=int)
argsparser.add_argument("-c","--curve",help="Specify with generator curve to use (default is in gstt.py)",type=int)
argsparser.add_argument("-r","--reset",help="Reset alignement values",action="store_true")
argsparser.add_argument("-l","--laser",help="Last digit of etherdream ip address 192.168.1.0/24 (4 by default). Localhost if digit provided is 0.",type=int)
argsparser.add_argument("-d","--display",help="Point list number displayed in pygame simulator",type=int)

args = argsparser.parse_args()


# Ports arguments
if args.iport:
	iport = args.iport
	gstt.iport = iport
else:
	iport = gstt.iport

if args.oport:
	oport = args.oport
	gstt.oport = oport
else:
	oport = gstt.oport

print "gstt.oport:",gstt.oport
print "gstt.iport:",gstt.iport


# X Y inversion arguments
if args.invx == True:

	gstt.swapx = -1 * gstt.swapx
	gstt.centerx = 0
	gstt.centery = 0
	WriteSettings()
	print("X invertion Asked")
	if gstt.swapx == 1:
		print ("X not Inverted")
	else:
		print ("X Inverted")

if args.invy == True:

	gstt.swapy = -1 * gstt.swapy
	gstt.centerx = 0
	gstt.centery = 0
	WriteSettings()
	print("Y invertion Asked")
	if gstt.swapy == 1:
		print ("Y not Inverted")
	else:
		print("Y inverted")



# Set / Curves arguments
if args.set != None:
	gstt.Set = args.set
	print "Set : " + str(gstt.Set)

if args.curve != None:
	gstt.Curve = args.curve
	print "Curve : " + str(gstt.Curve)


# Point list number used by simulator
if args.display  != None:
	gstt.simuPL = args.display
	
	
# Etherdream target
if args.laser  != None:
	lstdgtlaser = args.laser
	if lstdgtlaser == 0:
		etherIP = "127.0.0.1"
	else:
		etherIP = "192.168.1."+str(lstdgtlaser)

else:
	etherIP = "192.168.1.4"

print ("Laser 1 etherIP:",etherIP)

# Reset alignment values
if args.reset == True:

	gstt.centerx = 0
	gstt.centery = 0
	gstt.zoomx = 15
	gstt.zoomy = 15
	gstt.sizex = 32000
	gstt.sizey = 32000
	gstt.finangle = 0.0
	gstt.swapx = 1
	gstt.swapy = 1
	WriteSettings()
	
	
print ("Alignement settings loaded for Laser 1 ")
print ("Center x : " + str(gstt.centerx) + " Center Y : " + str(gstt.centery) + " Zoom X : " + str(gstt.zoomx) + " Zoom Y : " + str(gstt.zoomy) + " Size X :" + str(gstt.sizex) + " Size Y : " + str(gstt.sizey) + " Rotation Angle : " + str(gstt.finangle)  + "  Swap X : " + str(gstt.swapx) + "  Swap Y : " + str(gstt.swapy)+ " Set : " + str(gstt.Set) + "  Curve : " + str(gstt.Curve))



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
	#import nozoid



#dots = []

x = 0

settables =  {
        0: set0.Sine,
        1: set0.xPLS,
        2: set0.Orbits,
        3: set0.Dot,
        4: set0.Circle,
        5: set0.CC,
        6: set0.Orbits,
        7: set0.Slave
    }, {
        0: set1.LineX,
        1: set1.Sine,
        2: set1.Orbits,
        3: set1.Dot,
        4: set1.Circle,
        5: set1.CC,
        6: set1.Slave
    }, {
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

'''
def dac_thread0():
    while True:
        try:
            d1 = dac.DAC(gstt.lasersIPS[0])
            d1.play_stream(laser)
        except Exception as e:

            import sys, traceback
            if gstt.debug == 2:
                print '\n---------------------'
                print 'Exception: %s' % e
                print '- - - - - - - - - - -'
                traceback.print_tb(sys.exc_info()[2])
                print "\n"
            pass


def dac_thread1():
    while True:
        try:
            d1 = dac.DAC(gstt.lasersIPS[1])
            d1.play_stream(laser)
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
            d2 = dac.DAC(gstt.lasersIPS[2])
            d2.play_stream(laser)
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

#thread.start_new_thread(dac_thread, ())

thread.start_new_thread(dac_thread1, ())
print ""
print "dac thread 1 with IP : ", gstt.lasersIPS[1]," and point list : ", gstt.lasersPLS[1],

thread.start_new_thread(dac_thread2, ())
print ""
print "dac thread 2 with IP : ", gstt.lasersIPS[2]," and point list : ", gstt.lasersPLS[2],



update_screen = False
keystates = pygame.key.get_pressed()
(SCREEN_W, SCREEN_H) = screen_size


gstt.jumptable = settables[gstt.Set]


print ""
if gstt.SLAVERY != False:
	print "Node Slavery Mode : ", str(gstt.SLAVERY)
else: 
	print "Node Mode : MASTER"
print "Using Curve : ", str(gstt.Curve), " in Set : ", str(gstt.Set)
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




