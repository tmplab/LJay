#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# -*- mode: Python -*-

import math
import gstt
from globalVars import *
import bhorosc
import colorify
import orbits

f_sine = 0

# Curve 0
def LineX(fwork):

    joypads()
    # vertical line
    dots = []
    x = cc2scrX(gstt.cc[1]+1)
    y = 0
    dots.append((int(x),int(y)))
    dots.append((int(x),int(screen_size[1])))
    #print dots
    fwork.PolyLineOneColor(dots, c=colorify.rgb2hex(gstt.color))

    # horizontal line
    dots = []
    y = cc2scrY(gstt.cc[2]+1)
    x = 0       
    dots.append((int(x),int(y)))
    dots.append((int(screen_size[0]),int(y)))
    fwork.PolyLineOneColor(dots, c=colorify.rgb2hex(gstt.color))



# Curve 1
def Sine(fwork):
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

# Curve 2
def Orbits(fwork):

    orbits.Orbits.Draw(fwork)
   

# Curve 3	
def Dot(fwork):

    dots = []
    x = cc2scrX(gstt.cc[1])
    y = cc2scrY(gstt.cc[2])
    #x = xy_center[0] + gstt.cc[1]*amp    
    #y = xy_center[1] + gstt.cc[2]*amp
    print x,y,proj(int(x),int(y),0)
    dots.append(proj(int(x),int(y),0))
    dots.append(proj(int(x)+5,int(y)+5,0))
    
    fwork.PolyLineOneColor(dots, c=colorify.rgb2hex(gstt.color)  )

# Curve 4
def Circle(fwork):
    global f_sine

    dots = []
    amp = 200
    nb_point = 40
    for t in range(0, nb_point+1):
        y = 0 - amp*math.sin(2* PI * f_sine *(float(t)/float(nb_point)))
        x = 0 - amp*math.cos(2* PI * f_sine *(float(t)/float(nb_point)))
        dots.append(proj(int(x),int(y),0))

    fwork.PolyLineOneColor( dots, c=colorify.rgb2hex(gstt.color) )
    
    #print f_sine
    if f_sine > 24:
        f_sine = 0
    f_sine += 0.01
		

# Curve 5
def CC(fwork):

    dots = []
        
    amp = 200
    nb_point = 60
    for t in range(0, nb_point+1):
        y = 1 - amp*math.sin(2*PI*cc2range(gstt.cc[5],0,24)*(float(t)/float(nb_point)))
        x = 1 - amp*math.cos(2*PI*cc2range(gstt.cc[6],0,24)*(float(t)/float(nb_point))) 
        #bhorosc.send5("/point", [proj(int(x),int(y),0),colorify.rgb2hex(gstt.color)])       
        dots.append(proj(int(x),int(y),0))
        
    fwork.PolyLineOneColor( dots, c=colorify.rgb2hex(gstt.color) )



# Curve 6
def Slave(fwork):
    
    fwork.LineTo([gstt.point[0],gstt.point[1]],gstt.point[2])



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


# 3D rotation and 2D projection for a given 3D point
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
    x = x * factor +  xy_center [0] + gstt.cc[1] -100
    y = - y * factor +  xy_center [1] - gstt.cc[2]


    return x,y



def joypads():

	if gstt.SLAVERY == False and gstt.Nbpads > 0:
	
	
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
			gstt.cc[21] = 21 	#FOV
			gstt.cc[22] = gstt.surpriseon 	#Distance
			gstt.cc[2] +=  gstt.surprisey
			gstt.cc[1] +=  gstt.surprisex
			print "Surprise ON"
		
		#Bouton "3" 0 : surprise OFF
		
		if gstt.pad1.get_button(2) == 0:
			gstt.surprise = 0
			gstt.cc[21] = 21 	#FOV
			gstt.cc[22] = gstt.surpriseoff 	#Distance
			
		#Bouton "4". cycle couleur
		
		#if gstt.pad1.get_button(3) == 1:
		#	print "3", str(gstt.pad1.get_button(3))
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
			
			
		#Bouton "1"	: augmente Vitesse des planetes
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
		
		
		
		#Bouton "2"	augmente Nombre de planetes
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
		
		
		
		# hat droit	augmente Nombre de planetes
		#if gstt.pad1.get_hat(0)[0] == 1:
			#print "1", str(gstt.pad1.get_hat(0)[0])
		if gstt.pad1.get_hat(0)[0] == 1 and gstt.cc[6] < 125:
			gstt.cc[6] +=1
			print "Y Curve/nb de planetes : ",str(gstt.cc[6])
		
		#print "hat : ", str(gstt.pad1.get_hat(0)[1])

		
