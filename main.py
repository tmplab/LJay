#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# -*- mode: Python -*-

'''
Main test (Emvivre)

Inspired from Empty Laser (Sam Neurohack) 
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
from globalVars import *

import gstt
import sv
import colorify

import argparse

print ""
print "Arguments parsing if needed..."
#have to be done before importing bhorosc.py to get correct port assignment
argsparser = argparse.ArgumentParser(description="A Scanner Interface Darkly")
#argsparser.add_argument("interface",help="interface to scan")
argsparser.add_argument("-i","--iport",help="port number to listen to (8001 by default)",type=int)
argsparser.add_argument("-o","--oport",help="port number to send to (8002 by default)",type=int)
argsparser.add_argument("-l","--laser",help="Last digit of etherdream ip address 192.168.1.0/24 (4 by default)",type=int)

args = argsparser.parse_args()

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

if args.laser:
	lstdgtlaser = args.laser
else:
	lstdgtlaser = 4

#gsst.ports will be set in bhorosc
print "gstt.oport:",gstt.oport
print "gstt.iport:",gstt.iport

etherIP = "192.168.1."+str(lstdgtlaser)
print "etherIP:",etherIP
#raw_input("Hit Enter To Continue!")

import midi
import bhorosc
import set0
import set1
import setllstr
import modes
import orbits

if not gstt.SLAVERY :
	midi.InConfig()
	midi.OutConfig()
	#import nozoid



#dots = []

x = 0

settables =  {
        0: set0.Sine,
        1: set0.Sine,
        2: set0.Orbits,
        3: set0.Dot,
        4: set0.Circle,
        5: set0.CC,
        6: set0.Orbits,
        7: set0.Slave
    }, {
        0: set1.Sine,
        1: set1.Sine,
        2: set1.CC,
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



# Inits

app_path = os.path.dirname(os.path.realpath(__file__))

pygame.init()
screen = pygame.display.set_mode(screen_size)


if gstt.SLAVERY == False:

	pygame.display.set_caption("Laser Master")
	
	print ""
	Nbpads = pygame.joystick.get_count()
	print "Joypads : ", str(Nbpads)

	if Nbpads > 1:

		pad2 = pygame.joystick.Joystick(1)
		pad2.init()

		print pad2.get_name()
		print "Axis : ", str(pad2.get_numaxes())
		numButtons = pad2.get_numbuttons()
		print "Buttons : " , str(numButtons)

	if Nbpads > 0:

		pad1 = pygame.joystick.Joystick(0)
		pad1.init()

		print pad1.get_name()


		print "Axis : ", str(pad1.get_numaxes())
		numButtons = pad1.get_numbuttons()
		print "Buttons : " , str(numButtons)


	
else:
	pygame.display.set_caption("Laser Slave ",str(gstt.SLAVERY))

clock = pygame.time.Clock()


fwork_holder = frame.FrameHolder()
laser = renderer.LaserRenderer(fwork_holder, gstt.centerx, gstt.centery, gstt.zoomx, gstt.zoomy, gstt.sizex, gstt.sizey)
thread.start_new_thread(dac_thread, ())

update_screen = False
keystates = pygame.key.get_pressed()
(SCREEN_W, SCREEN_H) = screen_size


#gstt.jumptable =  settables[0]
gstt.jumptable =  settables[2]


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
		
	if gstt.SLAVERY == False and Nbpads > 0:
	
	
		# Champi gauche
		# Move center on X axis according to pad
		if pad1.get_axis(2)<-0.1 or pad1.get_axis(2)>0.1:
			gstt.cc[1] += -pad1.get_axis(2) * 2

		# Move center on Y axis according to pad
		if pad1.get_axis(3)<-0.1 or pad1.get_axis(3)>0.1:
			gstt.cc[2] += pad1.get_axis(3) * 2

		# Champi droite
		'''
		# Move center on X axis according to pad
		if pad1.get_axis(0)<-0.1 or pad1.get_axis(0)>0.1:
			gstt.cc[21] += -pad1.get_axis(0) * 2

		# Move center on Y axis according to pad
		if pad1.get_axis(1)<-0.1 or pad1.get_axis(1)>0.1:
			gstt.cc[22] += pad1.get_axis(1) * 2
		'''	
		# "1" pygame 0
		# "2" pygame 1
		# "3" pygame 2
		# "4" pygame 3
		# "L1" pygame 4
		# "L2" pygame 6
		# "R1" pygame 5
		# "R2" pygame 7
			
		# Hat gauche pad1.get_hat(0)[0] = -1
		# Hat droit  pad1.get_hat(0)[0] = 1

		# Hat bas pad1.get_hat(0)[1] = -1
		# Hat haut  pad1.get_hat(0)[1] = 1
		
				
		#Bouton "3" 1 : surprise ON
		
		if pad1.get_button(2) == 1 and gstt.surprise == 0:
			gstt.surprise = 1
			gstt.cc[21] = 21 	#FOV
			gstt.cc[22] = gstt.surpriseon 	#Distance
			gstt.cc[2] +=  gstt.surprisey
			gstt.cc[1] +=  gstt.surprisex
			print "Surprise ON"
		
		#Bouton "3" 0 : surprise OFF
		
		if pad1.get_button(2) == 0:
			gstt.surprise = 0
			gstt.cc[21] = 21 	#FOV
			gstt.cc[22] = gstt.surpriseoff 	#Distance
			
		#Bouton "4". cycle couleur
		
		#if pad1.get_button(3) == 1:
		#	print "3", str(pad1.get_button(3))
		'''
		if pad1.get_button(3) == 1:
			newcolor = random.randint(0,2)
			print newcolor
			
			if gstt.color[newcolor] == 0:
				gstt.color[newcolor] = 1
				
			else:
				gstt.color[newcolor] = 0
				
			print "Newcolor  : ",str(gstt.newcolor), " ", str(gstt.color[newcolor])
		
		'''
				
		'''
		#Bouton "3" : diminue Vitesse des planetes
		if pad1.get_button(2) == 1:
			print "2", str(pad1.get_button(2))
		if pad1.get_button(2) == 1 and gstt.cc[5] > 2:
			gstt.cc[5] -=1
			print "X Curve : ",str(gstt.cc[5])
			
			
		#Bouton "1"	: augmente Vitesse des planetes
		if pad1.get_button(0) == 1:
			print "0", str(pad1.get_button(0))
		if pad1.get_button(0) == 1 and gstt.cc[5] < 125:
			gstt.cc[5] +=1
			print "X Curve : ",str(gstt.cc[5])
			
			
		#Bouton "4". diminue Nombre de planetes
		if pad1.get_button(3) == 1:
			print "3", str(pad1.get_button(3))
		if pad1.get_button(3) == 1 and gstt.cc[6] > 2:
			gstt.cc[6] -=1
			print "Y Curve : ",str(gstt.cc[6])
		
		
		
		#Bouton "2"	augmente Nombre de planetes
		if pad1.get_button(1) == 1:
			print "1", str(pad1.get_button(1))
		if pad1.get_button(1) == 1 and gstt.cc[6] < 125:
			gstt.cc[6] +=1
			print "Y Curve : ",str(gstt.cc[6])
		
		'''


		# Hat bas : diminue Vitesse des planetes
		#if pad1.get_hat(0)[1] == -1:
			#print "2", str(pad1.get_hat(0)[1])
		if pad1.get_hat(0)[1] == -1 and gstt.cc[5] > 2:
			gstt.cc[5] -=1
			print "X Curve/vitesse planete : ",str(gstt.cc[5])
			
			
		#Hat haut : augmente Vitesse des planetes
		#if pad1.get_hat(0)[1] == 1:
			#print "0", str(pad1.get_hat(0)[1])
		if pad1.get_hat(0)[1] == 1 and gstt.cc[5] < 125:
			gstt.cc[5] +=1
			print "X Curve/Vitesse planete : ",str(gstt.cc[5])
			
			
		# hat Gauche. diminue Nombre de planetes
		#if pad1.get_hat(0)[0] == -1:
			#print "3", str(pad1.get_hat(0)[0])
		if pad1.get_hat(0)[0] == -1 and gstt.cc[6] > 2:
			gstt.cc[6] -=1
			print "Y Curve/ nombre planete : ",str(gstt.cc[6])
		
		
		
		# hat droit	augmente Nombre de planetes
		#if pad1.get_hat(0)[0] == 1:
			#print "1", str(pad1.get_hat(0)[0])
		if pad1.get_hat(0)[0] == 1 and gstt.cc[6] < 125:
			gstt.cc[6] +=1
			print "Y Curve/nb de planetes : ",str(gstt.cc[6])
		
		#print "hat : ", str(pad1.get_hat(0)[1])

			

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




