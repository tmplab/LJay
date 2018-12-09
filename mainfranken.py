#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# -*- mode: Python -*-

'''
LJay v0.8.0


Multi process Client 
You need serverp.py and redis running first.

No more multi threaded handlers for etherdreams (not efficient for multilasers on high multitasking computers)

Send point lists directly to the redis server. Needs LJay Server (serverp.py) to bridge redis <-> etherdreams


LICENCE : CC
Sam Neurohack, loloster, 

'''
#from __future__ import print_function 
import time 
import math
import random
import itertools
import sys
import os
import thread
import redis


print ""
print "LJay v0.8.0 Client"
print "Multilaser, multi process and redis style."
print ""
print "Needs redis and serverp.py launched to talk to etherdreams"
print ""
print "webui/index.html is the WebUI page"
print "Needs webui/uiserverp.py to talk to WebUI"
print ""
print "Autoconfiguring..."
print ""


#import renderer

import pygame
#import dac
# import newdac
#import newdacp
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

r = redis.StrictRedis(host=gstt.LjayServerIP, port=6379, db=0)

#raw_input("Hit Enter To Continue!")
#print "Simulator displays point list : ", str(gstt.simuPL)

import midi
import framep
import bhoroscp

import homographyp
import set0
import set1
import setllstrp
import setamiral
import setfranken
import setexample
import set5
import set6
import set7
import set8

import orbits
import alignp

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
        0: setllstrp.NozMode,
        1: setllstrp.NozMode2,
        2: setllstrp.Sine,
        3: setllstrp.Orbits,
        4: setllstrp.Circle,
        5: setllstrp.CC,
        6: setllstrp.Slave
    }, {                        # setfranken Set 3 (was setamiral)
        0: setfranken.Mapping,
        1: setfranken.Starfield,
        2: setfranken.Faces,
        3: setfranken.Dancers,
        4: setfranken.Pose

    }, {                        # setexample Set 4
        0: setexample.Mapping,
        1: setexample.Sine,
        2: setexample.xPLS,
        3: setexample.CC,
        4: setexample.Text,
        5: setexample.black
    }, {                        # setexample Set 5
        0: set5.square,
        1: set5.Sine
    }, {                        # setexample Set 6
        0: set6.square,
        1: set6.Sine
    }, {                        # setexample Set 7
        0: set7.square,
        1: set7.Sine
    }, {                        # setexample Set 8
        0: set8.square,
        1: set8.Sine
    }

gstt.MaxSets = len(settables)

# built in black dot when curve = -1. Will be called when set change.
def blackall():

    print "black out"
    for laserid in range(0,4):
        PL = laserid
        dots = []
        x = xy_center[0] 
        y = xy_center[1]
        dots.append((x,y))
        dots.append((x+5,y+5))
        print "black laser", laserid
        fwork.PolyLineOneColor(dots, c=colorify.rgb2hex([0,0,0]), PL = 0, closed = False)

    gstt.PL[PL] = fwork.LinesPL(PL)
   

# Inits

# Check if all required etherdreams are actually on the network if gstt.debug > 0
print ""
print "Settings require", gstt.LaserNumber, "lasers..." 
print "Generating homographies..."
for laser in xrange(gstt.LaserNumber):
    homographyp.newEDH(laser)
    #r.set('/EDH/'+str(laser), np.array2string(gstt.EDH[laser], separator=','))


# Ping check if debug > 1
if gstt.debug > 1:
	for lasercheck in xrange(gstt.LaserNumber):

		#print ""
		print "Checking...",gstt.lasersIPS[lasercheck],
		#if os.system("ping -c 1 -i 0.5 -q  " + gstt.lasersIPS[lasercheck]) != 0:
		if os.system("ping -c 1 -W 1 -q " + gstt.lasersIPS[lasercheck] + "> /dev/null 2>&1") != 0:
			#print ""
			#print gstt.lasersIPS[lasercheck], "IS NOT CONNECTED"
			print "which is not connected"
		else:
			#print ""
			#print gstt.lasersIPS[lasercheck], "IS OK"
			print "which is up and running !"


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

# Init calls

setfranken.preparePOSE()
setfranken.prepareFACES()
setfranken.prepareDANCERS()
setfranken.prepareSTARFIELD()

fwork_holder = framep.FrameHolder()

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


r.set('/resampler/0', '[ (1.0, 8),(0.25, 3), (0.75, 3), (1.0, 10)]')
r.set('/resampler/1', '[ (1.0, 8),(0.25, 3), (0.75, 3), (1.0, 10)]')
r.set('/resampler/2', '[ (1.0, 8),(0.25, 3), (0.75, 3), (1.0, 10)]')
r.set('/resampler/3', '[ (1.0, 8),(0.25, 3), (0.75, 3), (1.0, 10)]')

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
    fwork = framep.Frame()
	
    # align handler
    alignp.Jump(fwork)

    # Colorify
    colorify.jump()

    # Select and call the Curve to generate points, black() if Curve = -1

    #print gstt.starcount
    if gstt.starfieldcount == 1000000:
        gstt.Curve += -1

    if gstt.Curve != -1:
        gstt.jumptable = settables[gstt.Set]
        doit = gstt.jumptable.get(gstt.Curve)
        doit(fwork)
    else:
        blackall()

    # pending osc message ?
    bhoroscp.osc_frame()

    fwork_holder.f = fwork

    if update_screen:
    	update_screen = False
    	fwork.RenderScreen(screen)
    	pygame.display.flip()
    else:
    	update_screen = True

    clock.tick(30)
    # time.sleep(0.001)

pygame.quit()




