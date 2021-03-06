#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# -*- mode: Python -*-

'''
LJay v0.7.0

LICENCE : CC
Sam Neurohack, Loloster, 


'''
#from __future__ import print_function 
import time 
import math
import random
import itertools
import sys
import os
import thread


print ""
print "LJay v0.7.0"
print ""
print "Autoconfiguring..."
print ""

import frame
#import renderer


import pygame
import dac
import newdac
#import newrenderer
import settings
from globalVars import *

import gstt
import cli
import colorify
import pdb

settings.Read()

cli.handle()

settings.Write()

print ""
if gstt.debug == 0:
    print "NO DEBUG"
else:
    print "DEBUG : ", gstt.debug



#raw_input("Hit Enter To Continue!")
#print "Simulator displays point list : ", str(gstt.simuPL)

import midi

import bhorosc

import homography
import set0
import set1
import setllstr
import setamiral
import setexample
import set5
import set6
import set7
import set8


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
        4: set0.Sine,
        5: set0.Astro,
        6: set0.LaserID,
        7: set0.Pose
    }, {						# Set 1
        0: set1.Shapes,
        1: set1.Warp,
        2: set1.Pose,
        3: set1.LineX
    }, {						# setllstr Set 2
        0: setllstr.NozMode,
        1: setllstr.NozMode2,
        2: setllstr.Sine,
        3: setllstr.Orbits,
        4: setllstr.Circle,
        5: setllstr.CC,
        6: setllstr.Slave
    }, {                        # setamiral Set 3
        0: setamiral.Mapping,
        1: setamiral.Pose,
        2: setamiral.Faces,
        3: setamiral.Dancers
    }, {                        # setexample Set 4
        0: setexample.Mapping,
        1: setexample.Sine,
        2: setexample.xPLS,
        3: setexample.CC,
        4: setexample.Text
    }, {                        # setexample Set 5
        0: set5.Mapping,
        1: set5.Sine
    }, {                        # setexample Set 6
        0: set6.Mapping,
        1: set6.Sine
    }, {                        # setexample Set 7
        0: set7.Mapping,
        1: set7.Sine
    }, {                        # setexample Set 8
        0: set8.Mapping,
        1: set8.Sine,
    }
gstt.MaxSets = len(settables)

# built in black dot when curve = -1. Will be called when set change.
def black():

    print "black out"
    for laserid in range(0,4):
        PL = laserid
        dots = []
        x = xy_center[0] 
        y = xy_center[1]
        dots.append((x,y))
        dots.append((x+5,y+5))
        print "black"
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
            # newdac style
            d3 = newdac.DAC(3,gstt.lasersPLS[3])
            d3.play_stream()

            '''
            dac style
            d3 = dac.DAC(3,gstt.lasersPLS[3])
            d3.play_stream(laser)
            '''
        except Exception as e:

            import sys, traceback
            if gstt.debug == 2:
                print '\n---------------------'
                print 'Exception: %s' % e
                print '- - - - - - - - - - -'
                traceback.print_tb(sys.exc_info()[2])
                print "\n"
            pass



# Automated status sender
def dacstatus_thread():
    while True:
        try:
            while True:
                time.sleep(0.1)
                if bhorosc.oscdevice == 1:
                    for laserid in range(0,gstt.LaserNumber):           # Laser not used -> led is not lit

                        if gstt.lstt_dacstt[laserid] == 0:              # Dac IDLE state(0) -> led is blue (3)
                            bhorosc.sendosc("/lstt/" + str(laserid), 3)
                        if gstt.lstt_dacstt[laserid] == 1:              # Dac PREPARE state (1) -> led is cyan (2)
                            bhorosc.sendosc("/lstt/" + str(laserid), 2)
                        if gstt.lstt_dacstt[laserid] == 2:              # Dac PLAYING (2) -> led is green (1)
                            bhorosc.sendosc("/lstt/" + str(laserid), 1)

                        ''' This is not working : lack never change. Todo : understand why.
                        if gstt.lstt_dacanswers[laserid] == 'a':        # Dac sent ACK ("a") -> led is green (6)
                            bhorosc.sendosc("/lack/" + str(laserid), 6)
                        if gstt.lstt_dacanswers[laserid] == 'F':        # Dac sent FULL ("F") -> led is orange (5)
                            bhorosc.sendosc("/lack/" + str(laserid), 5)
                        if gstt.lstt_dacanswers[laserid] == 'I':        # Dac sent INVALID ("I") -> led is yellow (4)
                            bhorosc.sendosc("/lack/" + str(laserid), 4)
                        '''

                        if gstt.lstt_ipconn[laserid] != 0:              # no connection to dac -> leds are red (6)
                            bhorosc.sendosc("/lstt/" + str(laserid), 6)    
                        
                            #bhorosc.sendosc("/lack/" + str(laserid), 6)

                        # last number of points sent to etherdream buffer
                        bhorosc.sendosc("/points/" + str(laserid), gstt.lstt_points[laserid])

                    # WIP Too much packets -> flood webUI : Draw all PL point lists in JS canvas in WebUI
                    '''
                    for pl in range(0,1):   
                        bhorosc.sendosc("/plframe/" + str(pl),"")
                        for plpoint in range(0,len(gstt.PL[pl])):
                            bhorosc.sendosc("/plpoint/" + str(pl),"")
                    '''



        except Exception as e:
            import sys, traceback
            print '\n---------------------'
            print 'Exception: %s' % e
            print '- - - - - - - - - - -'
            traceback.print_tb(sys.exc_info()[2])
            print "\n"

# Inits

# Check if all required etherdreams are actually on the network if gstt.debug > 0
print ""
print "Settings require", gstt.LaserNumber, "lasers..." 
print "Generating homographies..."
for laser in xrange(gstt.LaserNumber):
    homography.newEDH(laser)

# Ping check if debug > 1
if gstt.debug > 1:
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
    print ""
    print "Display newdac points without etherdreams with debug mode -v 1 or 2"
    print "Pinging etherdreams is available with debug mode : -v 2"

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


if gstt.Curve == 0:

    # section 0 is "General", then first screen shapes in section 1
    # Todo : Should search automatically first screen in settings file sections.
    setexample.MappingConf(1)

if gstt.Set == 1 and gstt.Curve == 0:

    # section 0 is "General", then first screen shapes in section 1
    # Todo : Should search automatically first screen in settings file sections.
    set1.MappingConf(1)

clock = pygame.time.Clock()

# For Amiral

if gstt.Set == 3 and gstt.Curve == 1:
    setamiral.preparePOSE()

if gstt.Set == 3 and gstt.Curve == 2:
    setamiral.prepareFACES()

if gstt.Set == 3 and gstt.Curve == 3:
    setamiral.prepareDANCERS()


#gstt.PoseDir = '/Volumes/shared/openpose-1.3.0-win64-gpu-binaries/HeavyRain/2/json/'
#set0.selectPOSE('window1')

fwork_holder = frame.FrameHolder()
#laser = renderer.LaserRenderer(fwork_holder, gstt.centerx, gstt.centery, gstt.zoomx, gstt.zoomy, gstt.sizex, gstt.sizey)

# Start Dac threads

thread.start_new_thread(dac_thread0, ())
print ""
print "dac thread 0 with IP : ", gstt.lasersIPS[0]," and point list : ", gstt.lasersPLS[0],

if gstt.LaserNumber > 1:
    thread.start_new_thread(dac_thread1, ())
    print ""
    print "dac thread 1 with IP : ", gstt.lasersIPS[1]," and point list : ", gstt.lasersPLS[1],

if gstt.LaserNumber > 2:
    thread.start_new_thread(dac_thread2, ())
    print ""
    print "dac thread 2 with IP : ", gstt.lasersIPS[2]," and point list : ", gstt.lasersPLS[2],

if gstt.LaserNumber > 3:
    thread.start_new_thread(dac_thread3, ())
    print ""
    print "dac thread 2 with IP : ", gstt.lasersIPS[3]," and point list : ", gstt.lasersPLS[3],

'''
Old style launch with old dac.py
thread.start_new_thread(dac_thread3, ())
print ""
print "dac thread 3 with IP : ", gstt.lasersIPS[3]," and point list : ", gstt.lasersPLS[3],

'''

print "Dac Status OSC thread launch..."
# Launch Dac status OSC thread listening to Bhorosc
thread.start_new_thread(dacstatus_thread, ())


print ""


update_screen = False
keystates = pygame.key.get_pressed()
gstt.keystates = pygame.key.get_pressed()

(SCREEN_W, SCREEN_H) = screen_size

print "Set", gstt.Set, "has", len(settables[gstt.Set]), "Curves"
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

    # Maybe the Set has changed. So getting the new max number of Curve for the new Set
    # This is needed if the user ask for a non available Curve.
    # Refreshing at all times is stupid. Needs a better solution. Todo
    gstt.MaxCurves = len(settables[gstt.Set])
    
    
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
    time.sleep(0.001)

pygame.quit()




