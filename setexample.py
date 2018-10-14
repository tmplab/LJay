#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# -*- mode: Python -*-

'''
Laser Jaying

LICENCE : CC
Sam Neurohack, Loloster, 

setexample collect code examples to make your own generators that use LJay Laser management.

Curve 0 : Warp correction mode and "shapes" editor mode allowing to modify all points one by one.
Curve 1 : Sin Simple Lissajoux goes to Point List 0
Curve 2 : xPLS how to have different Point List generators to feed different lasers.
Curve 3 : CC how to use live inputs coming from midi.
Curve 4 : Text. Not working, work in progress.

'''


import math
import gstt
from globalVars import *
import bhorosc
import colorify
import numpy as np
import pdb
import time
from datetime import datetime
import settings


# For Mapping()
# dedicated settings handler is in settings.py
import pygame

f_sine = 0


# Curve 1
# Simple Lissajoux goes to Point List 0

def Sine(fwork):
    global f_sine

    PL = 1
    dots = []
    amp = 200
    nb_point = 40

    # "frame" components
    for t in range(0, nb_point+1):
        y = 0 - amp*math.sin(2 * PI * (float(t)/float(nb_point)))
        x = 0 - amp*math.cos(2 * PI * f_sine *(float(t)/float(nb_point)))
        dots.append(proj(int(x),int(y),0))

    fwork.PolyLineOneColor ( dots, c = colorify.rgb2hex(gstt.color), PL =  PL, closed = False)
    

    # after all frame components are sent :
    gstt.PL[PL] = fwork.LinesPL(PL)
    
    if f_sine > 24:
        f_sine = 0
    f_sine += 0.01



# Curve 2
# Multi laser example.

def xPLS(fwork):
    global f_sine


    # point list "PL" 0 generator (assigned to laser 0 in setexample.conf) 
    # middle horizontal line

    PL = 0
    dots = []
    x = (int(screen_size[1]) / 2) - 50
    y = (int(screen_size[0])/2)
    dots.append((int(x),int(y)))
    dots.append((int((int(screen_size[1]) / 2) + 50),(int(y))))
    fwork.PolyLineOneColor(dots, c=colorify.rgb2hex(gstt.color), PL = 0, closed = False)
    
    # after all needed PolyLineOneColor :
    gstt.PL[PL] = fwork.LinesPL(PL)
       



    # PL 1 generator (assigned to laser 1 in setexample.conf)
    # middle vertical line

    PL = 1
    dots = []
    #pdb.set_trace()
    x = int(screen_size[1]) / 2
    y = (int(screen_size[1])/2) -50
    dots.append((int(x),int(y)))
    dots.append((int(x),(int(screen_size[1])/2)+50))
    fwork.PolyLineOneColor(dots, c=colorify.rgb2hex(gstt.color), PL = 1, closed = False)
 
    # after all needed PolyLineOneColor are sent :
    gstt.PL[PL] = fwork.LinesPL(PL)
    
  

    # PL 2 generator (assigned to laser 2 in setexample.conf
    # Some Lissajoux function.
    PL = 2
    dots = []     
    amp = 200
    nb_point = 40
    for t in range(0, nb_point+1):
        y = 0 - amp*math.sin(2 * PI * (float(t)/float(nb_point)))
        x = 0 - amp*math.cos(2 * PI * f_sine *(float(t)/float(nb_point)))
        dots.append(proj(int(x),int(y),0))
    fwork.PolyLineOneColor ( dots, c = colorify.rgb2hex(gstt.color), PL =  2, closed = False)
    gstt.PL[PL] = fwork.LinesPL(PL)
    
    if f_sine > 24:
        f_sine = 0
    f_sine += 0.01




# Curve 3
# you can use live inputs. Here midi control change "CC" 5 and 6 are used. All live values are in gstt (gamestate) 
# CC value are 0-127 so there is function to remap to other values here cc2range()

def CC(fwork):

    PL = 0
    dots = []
        
    amp = 200
    nb_point = 60
    for t in range(0, nb_point+1):
        y = 1 - amp*math.sin(2*PI*cc2range(gstt.cc[5],0,24)*(float(t)/float(nb_point)))
        x = 1 - amp*math.cos(2*PI*cc2range(gstt.cc[6],0,24)*(float(t)/float(nb_point))) 
        dots.append(proj(int(x),int(y),0))

    # These points are generated in pygame coordinates space (0,0 is top left) defined by screen_size in globalVars.py
        
    fwork.PolyLineOneColor( dots, c=colorify.rgb2hex(gstt.color), PL = PL, closed = False )

    # you can also generate points around 0,0 and the use rPolyLineOneColor function like :
    # fwork.rPolyLineOneColor(dots, c=colorify.rgb2hex(gstt.color),  PL = 0, closed = False, xpos = 400, ypos = 300, resize = 50)


    gstt.PL[PL] = fwork.LinesPL(PL)



# Curve 4 WORK IN PROGRESS
def Text(fwork):
    
    fwork.LineTo([gstt.point[0],gstt.point[1]],gstt.point[2])



# examples to generate arrays of different types i.e for Lissajoux point lists generators.
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


# Curve 0
# Warp Mode / Edit shape mode 
# Interactive edition of shapes corners
# E     : Edit mode : cycle shapes/windows 
# Z     : next corner of current shape
# ENTER : Back to Warp mode that displays all shapes.
# A     : change "Screen"

def MappingConf(section):
    global mouse_prev, sections, warpd

    gstt.EditStep = 0
    gstt.CurrentWindow = -1
    gstt.CurrentCorner = 0
    gstt.CurrentSection = section
    mouse_prev = ((405, 325), (0, 0, 0))

    # Get all shapes points (="corners") for the given section of the conf file -> gstt.Windows 
    gstt.Windows = [] 
    sections = settings.MappingSections()

    print ""
    #print "Sections : ", sections
    print "Reading Section : ", sections[gstt.CurrentSection]

    gstt.Laser = settings.MappingRead([sections[gstt.CurrentSection],'laser'])
    print "Laser : ", gstt.Laser
    gstt.simuPL = gstt.Laser
    warpd = np.array(gstt.warpdest[gstt.Laser])

    for Window in xrange(settings.Mapping(sections[gstt.CurrentSection])-1):
        if gstt.debug > 0:
            print "Reading option :  ", str(Window)
        shape = [sections[gstt.CurrentSection], str(Window)]
        WindowPoints = settings.MappingRead(shape)
        gstt.Windows.append(WindowPoints)

    print "Section points : " ,gstt.Windows



def Mapping(fwork, keystates, keystates_prev):
    global mouse_prev, sections, warpd

    PL = gstt.Laser
    dots = []


    #switch to edit mode Key E ?
    if keystates[pygame.K_e] and not keystates_prev[pygame.K_e] and gstt.EditStep == 0:
            print "Switching to Edit Mode"
            gstt.EditStep = 1
            gstt.CurrentWindow = 0
            gstt.CurrentCorner = 0

    # Back to WARP mode if ENTER key is pressed ?
    if keystates[pygame.K_RETURN] and gstt.EditStep == 1:    
            
            print "Switching to Warp Mode"
            gstt.EditStep =0
            gstt.CurrentCorner = 0




    # EDIT MODE : cycle windows if press e key to adjust corner position 
    # Escape edit mode with enter key
    if gstt.EditStep >0:

        dots = []
        CurrentWindowPoints = gstt.Windows[gstt.CurrentWindow]

        # Draw all windows points or "corners"
        for corner in xrange(len(CurrentWindowPoints)):   
            dots.append(proj(int(CurrentWindowPoints[corner][0]),int(CurrentWindowPoints[corner][1]),0))
        fwork.PolyLineOneColor( dots, c=colorify.rgb2hex(gstt.color), PL = PL, closed = False )

        # Left mouse is clicked, modify current Corner coordinate
        if gstt.mouse[1][0] == mouse_prev[1][0] and mouse_prev[1][0] == 1:
            deltax = gstt.mouse[0][0]-mouse_prev[0][0]
            deltay = gstt.mouse[0][1]-mouse_prev[0][1]
            CurrentWindowPoints[gstt.CurrentCorner][0] += (deltax *2)
            CurrentWindowPoints[gstt.CurrentCorner][1] -= (deltay * 2)

        # Change corner if Z key is pressed.
        if keystates[pygame.K_z] and not keystates_prev[pygame.K_z]:
            if gstt.CurrentCorner < settings.Mapping(sections[gstt.CurrentSection]) - 1:
                gstt.CurrentCorner += 1
                print "Corner : ", gstt.CurrentCorner

        # Press E inside Edit mode : Next window 
        if keystates[pygame.K_e] and not keystates_prev[pygame.K_e]:

            # Save current Window and switch to the next one.
            if gstt.CurrentWindow < settings.Mapping(sections[gstt.CurrentSection]) -1:
                print "saving "
                settings.MappingWrite(sections,str(gstt.CurrentWindow),CurrentWindowPoints)
                gstt.CurrentWindow += 1
                gstt.CurrentCorner = -1
                if gstt.CurrentWindow == settings.Mapping(sections[gstt.CurrentSection]) -1:
                    gstt.EditStep == 0
                    gstt.CurrentWindow = 0              
                print "Now Editing window ", gstt.CurrentWindow

        mouse_prev = gstt.mouse
        gstt.PL[PL] = fwork.LinesPL(PL)

    # Press A : Next section ?
    if keystates[pygame.K_a] and not keystates_prev[pygame.K_a]: 
            
        print "current section : ", gstt.CurrentSection
        if gstt.CurrentSection < len(sections)-1:
            gstt.CurrentSection += 1
            print "Next section name is ", sections[gstt.CurrentSection]
            if "screen" in sections[gstt.CurrentSection]:
                print ""
                print "switching to section ", gstt.CurrentSection, " ", sections[gstt.CurrentSection]
                MappingConf(gstt.CurrentSection)
        else:
             gstt.CurrentSection = -1
        



    # WARP Mode
    if gstt.EditStep == 0:
        
        #print "Warp mode"
        # Left mouse is clicked, modify current Corner coordinate
        #print gstt.mouse
        if gstt.mouse[1][0] == mouse_prev[1][0] and mouse_prev[1][0] == 1:
            deltax = gstt.mouse[0][0]-mouse_prev[0][0]
            deltay = gstt.mouse[0][1]-mouse_prev[0][1]
            
            print "Laser ", gstt.Laser, " Corner ", gstt.CurrentCorner, "deltax ", deltax, "deltay", deltay
            #int(gstt.warpdest[gstt.Laser][gstt.CurrentCorner][0]) += (deltax *20)
            #int(gstt.warpdest[gstt.Laser][gstt.CurrentCorner][1]) += (deltay * 2)
            
            print warpd

            #print int(gstt.warpdest[gstt.Laser][gstt.CurrentCorner][0]) + (deltax * 20)
        # Change corner if Z key is pressed.
        if keystates[pygame.K_z] and not keystates_prev[pygame.K_z]:
            if gstt.CurrentCorner < 4:
                gstt.CurrentCorner += 1
                print "Corner : ", gstt.CurrentCorner


        # Display all windows to current PL for display
        for Window in gstt.Windows:  

            dots = []
            for corner in xrange(len(Window)):   
                #print "Editing : ", WindowPoints[corner]
                #print Window[corner][0]
                dots.append(proj(int(Window[corner][0]),int(Window[corner][1]),0))
            
            fwork.PolyLineOneColor( dots, c=colorify.rgb2hex(gstt.color), PL = PL, closed = False  )
    
        gstt.PL[PL] = fwork.LinesPL(PL)

        mouse_prev = gstt.mouse


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


def joypads():

    if gstt.Nbpads > 0:
        
        # Champi gauche
        # Move center on X axis according to pad
        if gstt.pad1.get_axis(2)<-0.1 or gstt.pad1.get_axis(2)>0.1:
            gstt.cc[1] += gstt.pad1.get_axis(2) * 2

        # Move center on Y axis according to pad
        if gstt.pad1.get_axis(3)<-0.1 or gstt.pad1.get_axis(3)>0.1:
            gstt.cc[2] += gstt.pad1.get_axis(3) * 2

        # Champi droite
        '''
        # Change FOV according to joypad
        if gstt.pad1.get_axis(0)<-0.1 or gstt.pad1.get_axis(0)>0.1:
            gstt.cc[21] += -gstt.pad1.get_axis(0) * 2

        # Change dist according to pad
        if gstt.pad1.get_axis(1)<-0.1 or gstt.pad1.get_axis(1)>0.1:
            gstt.cc[22] += gstt.pad1.get_axis(1) * 2
        ''' 
        # "1" pygame 0
        # "2" pygame 1
        # "3" pygame 2
        # "4" pygame 3
        # "L1" pygame 4
        # "L2" pygame 6
        # "R1" pygame 5
        # "R2" pygame 7
            
        # Hat gauche gstt.pad1.get_hat(0)[0] = -1
        # Hat droit  gstt.pad1.get_hat(0)[0] = 1

        # Hat bas gstt.pad1.get_hat(0)[1] = -1
        # Hat haut  gstt.pad1.get_hat(0)[1] = 1
        
                
        #Bouton "3" 1 : surprise ON
        
        if gstt.pad1.get_button(2) == 1 and gstt.surprise == 0:
            gstt.surprise = 1
            gstt.cc[21] = 21    #FOV
            gstt.cc[22] = gstt.surpriseon   #Distance
            gstt.cc[2] +=  gstt.surprisey
            gstt.cc[1] +=  gstt.surprisex
            print "Surprise ON"
        
        #Bouton "3" 0 : surprise OFF
        
        if gstt.pad1.get_button(2) == 0:
            gstt.surprise = 0
            gstt.cc[21] = 21    #FOV
            gstt.cc[22] = gstt.surpriseoff  #Distance
            
        #Bouton "4". cycle couleur
        
        #if gstt.pad1.get_button(3) == 1:
        #   print "3", str(gstt.pad1.get_button(3))
        '''
        if gstt.pad1.get_button(3) == 1:
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
        if gstt.pad1.get_button(2) == 1:
            print "2", str(gstt.pad1.get_button(2))
        if gstt.pad1.get_button(2) == 1 and gstt.cc[5] > 2:
            gstt.cc[5] -=1
            print "X Curve : ",str(gstt.cc[5])
            
            
        #Bouton "1" : augmente Vitesse des planetes
        if gstt.pad1.get_button(0) == 1:
            print "0", str(gstt.pad1.get_button(0))
        if gstt.pad1.get_button(0) == 1 and gstt.cc[5] < 125:
            gstt.cc[5] +=1
            print "X Curve : ",str(gstt.cc[5])
            
            
        #Bouton "4". diminue Nombre de planetes
        if gstt.pad1.get_button(3) == 1:
            print "3", str(gstt.pad1.get_button(3))
        if gstt.pad1.get_button(3) == 1 and gstt.cc[6] > 2:
            gstt.cc[6] -=1
            print "Y Curve : ",str(gstt.cc[6])
        
        
        
        #Bouton "2" augmente Nombre de planetes
        if gstt.pad1.get_button(1) == 1:
            print "1", str(gstt.pad1.get_button(1))
        if gstt.pad1.get_button(1) == 1 and gstt.cc[6] < 125:
            gstt.cc[6] +=1
            print "Y Curve : ",str(gstt.cc[6])
        
        '''


        # Hat bas : diminue Vitesse des planetes
        #if gstt.pad1.get_hat(0)[1] == -1:
            #print "2", str(gstt.pad1.get_hat(0)[1])
        if gstt.pad1.get_hat(0)[1] == -1 and gstt.cc[5] > 2:
            gstt.cc[5] -=1
            print "X Curve/vitesse planete : ",str(gstt.cc[5])
            
            
        #Hat haut : augmente Vitesse des planetes
        #if gstt.pad1.get_hat(0)[1] == 1:
            #print "0", str(gstt.pad1.get_hat(0)[1])
        if gstt.pad1.get_hat(0)[1] == 1 and gstt.cc[5] < 125:
            gstt.cc[5] +=1
            print "X Curve/Vitesse planete : ",str(gstt.cc[5])
            
            
        # hat Gauche. diminue Nombre de planetes
        #if gstt.pad1.get_hat(0)[0] == -1:
            #print "3", str(gstt.pad1.get_hat(0)[0])
        if gstt.pad1.get_hat(0)[0] == -1 and gstt.cc[6] > 2:
            gstt.cc[6] -=1
            print "Y Curve/ nombre planete : ",str(gstt.cc[6])
        
        
        
        # hat droit augmente Nombre de planetes
        #if gstt.pad1.get_hat(0)[0] == 1:
            #print "1", str(gstt.pad1.get_hat(0)[0])
        if gstt.pad1.get_hat(0)[0] == 1 and gstt.cc[6] < 125:
            gstt.cc[6] +=1
            print "Y Curve/nb de planetes : ",str(gstt.cc[6])
        
        #print "hat : ", str(gstt.pad1.get_hat(0)[1])

        

