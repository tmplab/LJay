#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# -*- mode: Python -*-

'''
LJay v0.8.0

Mainy : 
Provides a multi laser system (webui, control of n etherdreams, OSC, midi, joypads,...)
Multi process style
You need redis-server and to write launch separately a client to generate a point list per laset, see clients directory.

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
import redis


print ""
print "LJay v0.8.0 Mainy"
print "Multilaser, multi process and redis style."
print ""
print "Needs a laser setup configuration file mainy.conf"
print "Autoconfiguring..."
print ""


import pygame
import settings
from globalVars import *

import gstt
import cli
import pdb
import redis


settings.Read()

cli.handle()

settings.Write()

print ""
if gstt.debug == 0:
    print "NO DEBUG"
else:
    print "DEBUG : ", gstt.debug

r = redis.StrictRedis(host=gstt.LjayServerIP, port=6379, db=0)

import midi
import framep
import bhoroscp

import homographyp
import alignp

midi.InConfig()
midi.OutConfig()
 
x = 0

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

fwork_holder = framep.FrameHolder()

print ""


update_screen = False
keystates = pygame.key.get_pressed()
gstt.keystates = pygame.key.get_pressed()

(SCREEN_W, SCREEN_H) = screen_size


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


    screen.fill(0)
    fwork = framep.Frame()
	
    # align handler
    alignp.Jump(fwork)

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




