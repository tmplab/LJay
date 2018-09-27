#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# -*- mode: Python -*-

'''
LJay v0.6.2

LICENCE : CC
Sam Neurohack, Loloster, 


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
import newrenderer
import settings
from globalVars import *

import gstt
import cli
import colorify
import pdb

print ""
print "LJay"
print ""
print "Autoconfiguring..."

print ""
if gstt.debug == 0:
	print "NO DEBUG"
else:
	print "DEBUG : ", gstt.debug


settings.Read()

cli.handle()

settings.Write()

#raw_input("Hit Enter To Continue!")
#print "Simulator displays point list : ", str(gstt.simuPL)

import midi

import bhorosc

import set0

import set1
import setllstr
import setamiral

import orbits
import align

midi.InConfig()
midi.OutConfig()

x = 0

# Curves Jump tables

settables =  {					# Set 0
        0: set0.Mapping,
        1: set0.xPLS,
        2: set0.Orbits,
        3: set0.Dot,
        4: set0.Circle,
        5: set0.CC,
        6: set0.Sine,
        7: set0.Astro,
        8: set0.Text,
        9: set0.Pose
    }, {						# Set 1
        0: set1.Shapes,
        1: set1.Warp,
        2: set1.Pose,
        3: set1.LineX
    }, {						# setllstr
        0: setllstr.NozMode,
        1: setllstr.NozMode2,
        2: setllstr.Sine,
        3: setllstr.Orbits,
        4: setllstr.Circle,
        5: setllstr.CC,
        6: setllstr.Slave
    }, {                        # setamiral
        0: setamiral.Mapping,
        1: setamiral.Pose,
        2: setamiral.Faces,
        3: setamiral.Dancers
    }

# built in black dot when curve = -1. Will be called when set change.
def black():
    PL = 0
    dots = []
    x = xy_center[0] 
    y = xy_center[1]
    dots.append(proj(int(x),int(y),0))
    dots.append(proj(int(x)+5,int(y)+5,0))
      
    fwork.PolyLineOneColor(dots, c=colorify.rgb2hex([0,0,0]), PL = 0, closed = False)
    gstt.PL[PL] = fwork.LinesPL(PL)

       
def dac_thread0():
    while True:
        try:
            d0 = newdac.DAC(0,gstt.lasersPLS[0])
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

def dac_thread1():
    while True:
        try:

            d1 = newdac.DAC(1,gstt.lasersPLS[1])
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
            d2 = newdac.DAC(2,gstt.lasersPLS[2])
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
            d3 = dac.DAC(3,gstt.lasersPLS[3])
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



# Inits

# Check if all required etherdreams are actually on the network if gstt.debug > 0
print ""
print "Settings require", gstt.LaserNumber, "lasers..." 
print "Generating homographies..."
for laser in xrange(gstt.LaserNumber):
    newrenderer.newEDH(laser)
    print "laser"+str(laser)
    print gstt.EDH[laser]

# Ping check if debug > 0
if gstt.debug > 0:
	for lasercheck in xrange(gstt.LaserNumber):

		print ""

		print "Checking... ", gstt.lasersIPS[lasercheck]
		if os.system("ping -c 1 -i 0.5 -q  " + gstt.lasersIPS[lasercheck]) != 0:
			print ""
			print gstt.lasersIPS[lasercheck], "IS NOT CONNECTED"
		else:
			print ""
			print gstt.lasersIPS[lasercheck], "IS OK"


else:
	print "Checking is available with debug mode : -v 1 or 2"

print ""

app_path = os.path.dirname(os.path.realpath(__file__))

pygame.init()
screen = pygame.display.set_mode(screen_size)


pygame.display.set_caption("LJay")


# Joypads check 	

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


if gstt.Set == 0 and gstt.Curve == 0:

    # section 0 is "General", then first screen shapes in section 1
    # Todo : Should search automatically first screen in settings file sections.
    set0.MappingConf(1)

if gstt.Set == 1 and gstt.Curve == 0:

    # section 0 is "General", then first screen shapes in section 1
    # Todo : Should search automatically first screen in settings file sections.
    set1.MappingConf(1)

clock = pygame.time.Clock()

# For Amiral

if gstt.Set == 3 and gstt.Curve == 2:

    #setamiral.preparePOSE()
    setamiral.prepareFACES()

if gstt.Set == 3 and gstt.Curve == 3:

    setamiral.prepareDANCERS()


#gstt.PoseDir = '/Volumes/shared/openpose-1.3.0-win64-gpu-binaries/HeavyRain/2/json/'
#set0.selectPOSE('window1')

fwork_holder = frame.FrameHolder()
laser = renderer.LaserRenderer(fwork_holder, gstt.centerx, gstt.centery, gstt.zoomx, gstt.zoomy, gstt.sizex, gstt.sizey)



# Start Dac threads

thread.start_new_thread(dac_thread0, ())
print ""
print "dac thread 0 with IP : ", gstt.lasersIPS[0]," and point list : ", gstt.lasersPLS[0],


thread.start_new_thread(dac_thread1, ())
print ""
print "dac thread 1 with IP : ", gstt.lasersIPS[1]," and point list : ", gstt.lasersPLS[1],


thread.start_new_thread(dac_thread2, ())
print ""
print "dac thread 2 with IP : ", gstt.lasersIPS[2]," and point list : ", gstt.lasersPLS[2],

'''
thread.start_new_thread(dac_thread3, ())
print ""
print "dac thread 2 with IP : ", gstt.lasersIPS[3]," and point list : ", gstt.lasersPLS[3],

'''
print ""



update_screen = False
keystates = pygame.key.get_pressed()
gstt.keystates = pygame.key.get_pressed()

(SCREEN_W, SCREEN_H) = screen_size


gstt.jumptable = settables[gstt.Set]


print ""

settings.Write()

print ""
print "Starting Main Loop..."


# Main loop

while True:

    # Pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break

    gstt.mouse = (pygame.mouse.get_pos(), pygame.mouse.get_pressed())
    keystates_prev = keystates[:]
    gstt.keystates_prev = gstt.keystates[:]
    keystates = pygame.key.get_pressed()[:]
    gstt.keystates = pygame.key.get_pressed()[:]


    if keystates[pygame.K_ESCAPE]:
        break

    screen.fill(0)
    fwork = frame.Frame()
	
    # align handler
    align.Jump(fwork)

    # Colorify
    colorify.jump()

    # Select and call the Curve to generate points, black() if Curve = -1

    if gstt.Curve != -1:
        gstt.jumptable = settables[gstt.Set]
        doit = gstt.jumptable.get(gstt.Curve)
        doit(fwork)
    else:
        black()

    # pending osc message ?
    bhorosc.osc_frame()


    fwork_holder.f = fwork

    if update_screen:
    	update_screen = False
    	fwork.RenderScreen(screen)
    	pygame.display.flip()
    else:
    	update_screen = True

    clock.tick(60)
    time.sleep(0.0001)

pygame.quit()




