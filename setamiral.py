#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# -*- mode: Python -*-

'''
Laser Jaying

LICENCE : CC
Sam Neurohack, Loloster, 

Set for amiral castle

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



# Curve 0
# Edit shape mode / Run Mode

def MappingConf(section):
    global mouse_prev, sections

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

    for Window in xrange(settings.Mapping(sections[gstt.CurrentSection])-1):
        print "Reading option :  ", str(Window)
        shape = [sections[gstt.CurrentSection], str(Window)]
        WindowPoints = settings.MappingRead(shape)
        gstt.Windows.append(WindowPoints)

    print "Section points : " ,gstt.Windows


print ""
print "For Mapping(), reading Architecture Points from set0.conf"

# section 0 is "General", then first screen shapes in section 1
# Todo : Should search automatically first screen in settings file sections.
MappingConf(1)


def Mapping(fwork, keystates, keystates_prev):
    global mouse_prev, sections

    PL = gstt.Laser
    dots = []

    #switch to edit mode Key E ?
    if keystates[pygame.K_e] and not keystates_prev[pygame.K_e] and gstt.EditStep == 0:
            print "Switching to Edit Mode"
            gstt.EditStep = 1
            gstt.CurrentWindow = 0
            gstt.CurrentCorner = 0

    # Back to normal if ENTER key is pressed ?
    if keystates[pygame.K_RETURN] and gstt.EditStep == 1:    
            
            print "Switching to Run Mode"
            gstt.EditStep =0



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
        

    # RUN MODE
    if gstt.EditStep == 0:
        
        # Add all windows to PL for display
        for Window in gstt.Windows:  

            dots = []
            for corner in xrange(len(Window)):   
                #print "Editing : ", WindowPoints[corner]
                #print Window[corner][0]
                dots.append(proj(int(Window[corner][0]),int(Window[corner][1]),0))
            
            fwork.PolyLineOneColor( dots, c=colorify.rgb2hex(gstt.color), PL = PL, closed = False  )
    
        gstt.PL[PL] = fwork.LinesPL(PL)






# Curve 1
import json
gstt.CurrentPose = 1

# get absolute body position points
def getCOCO(d,posepoints):
    
    dots = []
    for dot in posepoints:
        if len(d['part_candidates'][0][str(dot)]) != 0:
            dots.append((d['part_candidates'][0][str(dot)][0], d['part_candidates'][0][str(dot)][1]))
    return dots


# get relative (-1 0 1) body position points. a position -1, -1 means doesn't exist
def getBODY(d,posepoints):

    dots = []
    for dot in posepoints:
        print posepoints
        if len(d['people'][0]['pose_keypoints_2d']) != 0:
            if d['people'][0]['pose_keypoints_2d'][dot * 3] != -1 and  d['people'][0]['pose_keypoints_2d'][(dot * 3)+1] != -1:
                dots.append((d['people'][0]['pose_keypoints_2d'][dot * 3], d['people'][0]['pose_keypoints_2d'][(dot * 3)+1]))
    return dots


# get absolute face position points 
def getFACE(d,posepoints):

    dots = []
    for dot in posepoints:

        if len(d['people'][0]['face_keypoints_2d']) != 0:
            if d['people'][0]['face_keypoints_2d'][dot * 3] != -1 and  d['people'][0]['face_keypoints_2d'][(dot * 3)+1] != -1:
                dots.append((d['people'][0]['face_keypoints_2d'][dot * 3], d['people'][0]['face_keypoints_2d'][(dot * 3)+1]))
    return dots


# Body parts
def bodyCOCO(d):
    posepoints = [10,9,8,1,11,12,13]
    return getBODY(d,posepoints)

def armCOCO(d):
    posepoints = [7,6,5,1,2,3,4]
    return getBODY(d,posepoints)

def headCOCO(d):
    posepoints = [1,0]
    return getBODY(d,posepoints)


# Face keypoints
def face(d):
    posepoints = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
    return getFACE(d,posepoints)

def browL(d):
    posepoints = [26,25,24,23,22]
    return getFACE(d,posepoints)

def browR(d):
    posepoints = [21,20,19,18,17]
    return getFACE(d,posepoints)

def eyeR(d):
    posepoints = [36,37,38,39,40,41,36]
    return getFACE(d,posepoints)

def eyeL(d):
    posepoints = [42,43,44,45,46,47,42]
    return getFACE(d,posepoints)

def nose(d):
    posepoints = [27,28,29,30]
    return getFACE(d,posepoints)

def mouth(d):
    posepoints = [48,59,58,57,56,55,54,53,52,51,50,49,48,60,67,66,65,64,63,62,61,60]
    return getFACE(d,posepoints)


# best order face : face browL browr eyeR eyeL nose mouth

import os 


# Get frame number for pose path describe in gstt.PoseDir 
def selectPOSE(pose_dir):

    print "Check directory ",'poses/' + pose_dir + '/'
    numfiles = sum(1 for f in os.listdir('poses/' + pose_dir + '/') if os.path.isfile(os.path.join('poses/' + pose_dir + '/', f)) and f[0] != '.')
    print "Pose : ", pose_dir, numfiles, "images"
    return numfiles


def preparePOSE():


    # anim format (name, xpos,ypos, resize, currentframe, totalframe, count, speed)
    # total frame is fetched from directory file count
    
    anims1 = [['sky',50,400,100,0,0],['snap', 400,200, 50,0,0],['window1',100,200,100,0,0]]
    anims2 = [['window1', 400,200, 200,0,0],['snap',100,200,50,0,0]]
    
    for anim in anims2:
        anim[5]= selectPOSE(anim[0])
    gstt.anims0 = anims2

# display the pose animation describe in gstt.PoseDir
def Pose(fwork):
   
    for anim in gstt.anims0:
        PL = 0
        dots = []

        # repeat anim[8] time the same frame
        anim[6] +=1
        if anim[6] == anim[7]:

            anim[6] = 0
            # increase current frame and compare to total frame 
            anim[4] += 1
            if anim[4] == anim[5]:
                anim[4] = 0


        posename = 'poses/' + anim[0] + '/' + anim[0] +'-'+str("%05d"%anim[4])+'.json'
        posefile = open(posename , 'r') 
        posedatas = posefile.read()
        pose = json.loads(posedatas)

        fwork.rPolyLineOneColor(bodyCOCO(pose), c=colorify.rgb2hex(gstt.color), PL = 0, closed = False, xpos = anim[1], ypos = anim[2], resize = anim[3])
        fwork.rPolyLineOneColor(armCOCO(pose), c=colorify.rgb2hex(gstt.color), PL = 0, closed = False, xpos = anim[1], ypos = anim[2], resize = anim[3])
        fwork.rPolyLineOneColor(headCOCO(pose), c=colorify.rgb2hex(gstt.color),  PL = 0, closed = False, xpos = anim[1], ypos = anim[2], resize = anim[3])

        # Face
        '''
        #fwork.rPolyLineOneColor(face(pose), c=colorify.rgb2hex(gstt.color),  PL = 0, closed = False, xpos = anim[1], ypos = anim[2], resize = anim[3])
        fwork.rPolyLineOneColor(browL(pose), c=colorify.rgb2hex(gstt.color), PL = 0, closed = False, xpos = anim[1], ypos = anim[2], resize = anim[3])
        fwork.rPolyLineOneColor(browR(pose), c=colorify.rgb2hex(gstt.color), PL = 0, closed = False, xpos = anim[1], ypos = anim[2], resize = anim[3])
        fwork.rPolyLineOneColor(eyeR(pose), c=colorify.rgb2hex(gstt.color), PL = 0, closed = False, xpos = anim[1], ypos = anim[2], resize = anim[3])
        fwork.rPolyLineOneColor(eyeL(pose), c=colorify.rgb2hex(gstt.color), PL = 0, closed = False, xpos = anim[1], ypos = anim[2], resize = anim[3])
        fwork.rPolyLineOneColor(nose(pose), c=colorify.rgb2hex(gstt.color), PL = 0, closed = False, xpos = anim[1], ypos = anim[2], resize = anim[3])  
        fwork.rPolyLineOneColor(mouth(pose), c=colorify.rgb2hex(gstt.color), PL = 0, closed = False, xpos = anim[1], ypos = anim[2], resize = anim[3])
        '''

        gstt.PL[PL] = fwork.LinesPL(PL)


    
    time.sleep(0.02)
    '''
    # decrease current frame 
    if gstt.keystates[pygame.K_w]: # and not gstt.keystates_prev[pygame.K_w]:
        gstt.CurrentPose -= 1
        if gstt.CurrentPose < 2:
            gstt.CurrentPose = gstt.numfiles -1
        #time.sleep(0.033) 
        print "Frame : ",gstt.CurrentPose 

    # increaser current frame
    if gstt.keystates[pygame.K_x]: # and not gstt.keystates_prev[pygame.K_x]:
        gstt.CurrentPose += 1
        if gstt.CurrentPose > gstt.numfiles -1:
            gstt.CurrentPose = 1
        #time.sleep(0.033)
        print "Frame : ",gstt.CurrentPose 
    '''

