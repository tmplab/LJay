#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# -*- mode: Python -*-

import math
import gstt
from globalVars import *
import bhorosc
import colorify
import orbits
import numpy as np
import collections
import time

dotsosc0 = [collections.deque(maxlen=10)] * gstt.maxCurvesByLaser
dotsosc1 = [collections.deque(maxlen=10)] * gstt.maxCurvesByLaser
#dotsoscT = [dotsosc0,dotsosc1] * gstt.maxCurvesByLaser
dotsoscT = [dotsosc0,dotsosc1]
#dotsoscT = [collections.deque(maxlen=10),collections.deque(maxlen=10)] * gstt.maxCurvesByLaser
currentdotsosc = [0] * gstt.maxCurvesByLaser

#dotsosc0a = collections.deque(maxlen=10)
#dotsosc1a = collections.deque(maxlen=10)
#dotsoscTa = [dotsosc0a,dotsosc1a]
#currentdotsosca=0

f_sine = 0

screenSizeX=screen_size[0]
screenSizeY=screen_size[1]

# Curve 0
def NozMode(fwork):
    global f_sine,x

#    global dotsosc0
#    global dotsosc1
    global dotsoscT
    global currentdotsosc

#    global dotsosc0a
#    global dotsosc1a
#    global dotsoscTa
#    global currentdotsosca
        
    amp = 200
    nb_point = 40
    nbplow=10
    nbphigh=100

    # There is a sound curve to draw on X axis
    for curveNumber in range (0, gstt.maxCurvesByLaser): 
      if gstt.X[curveNumber] != 0:
    	#print "gstt.X != 0 (== %d)" % gstt.X
       	#if (dotsosc.maxlen == nbphigh and gstt.Y != 0):
       	if (dotsoscT[currentdotsosc[curveNumber]][curveNumber].maxlen == nbphigh and gstt.Y[curveNumber] != 0):
          #shrink points list (it's a lissajou curve)
          print "X changing size of dotsocsT[%d][%d] (%d) to %d"%(curveNumber,currentdotsosc[curveNumber],dotsoscT[currentdotsosc[curveNumber]][curveNumber].maxlen,nbplow)
          dotsoscT[currentdotsosc[curveNumber]][curveNumber] = collections.deque(maxlen=nbplow)
        xT = gstt.osc[gstt.X[curveNumber]]
        x = 3.5 * (extracc2scrX(xT) - screenSizeX/2)
    
      else:
        # Else (i.e. gstt.X == 0) use time for X axis and expand points list
        #print "gstt.X == 0"
        if (gstt.Y[curveNumber] != 0 and dotsoscT[currentdotsosc[curveNumber]][curveNumber].maxlen == nbplow):
          print "X changing size of dotsocsT[%d][%d] (%d) to %d"%(curveNumber,currentdotsosc[curveNumber],dotsoscT[currentdotsosc[curveNumber]][curveNumber].maxlen,nbphigh)
          dotsoscT[currentdotsosc[curveNumber]][curveNumber] = collections.deque(maxlen=nbphigh)
        xT = (((time.time()*50000) % 65536) - 32768)
        x = 3.5 * (extracc2scrX(xT) - screenSizeX/2)

      # There is a sound curve to draw on Y axis
      if gstt.Y[curveNumber] != 0:
        #print "gstt.Y != 0 (== %d)" % gstt.Y
        if (dotsoscT[currentdotsosc[curveNumber]][curveNumber].maxlen == nbphigh and gstt.X[curveNumber] != 0):
          print "Y changing size of dotsocsT[%d][%d] (%d) to %d"%(curveNumber,currentdotsosc[curveNumber],dotsoscT[currentdotsosc[curveNumber]][curveNumber].maxlen,nbplow)
          dotsoscT[currentdotsosc[curveNumber]][curveNumber] = collections.deque(maxlen=nbplow)
        yT = gstt.osc[gstt.Y[curveNumber]]
        y = 3.5 * (extracc2scrY(yT) - screenSizeY/2)
      else:
        # Use time for X axis    
        #print "gstt.Y == 0"
        if (gstt.X[curveNumber] != 0 and dotsoscT[currentdotsosc[curveNumber]][curveNumber].maxlen == nbplow):
          print "Y changing size of dotsocsT[%d][%d] (%d) to %d"%(curveNumber,currentdotsosc[curveNumber],dotsoscT[currentdotsosc[curveNumber]][curveNumber].maxlen,nbphigh)
          dotsoscT[currentdotsosc[curveNumber]][curveNumber] = collections.deque(maxlen=nbphigh)
        yT = (((time.time()*50000) % 65536) - 32768)
        y = 3.5 * (extracc2scrY(yT) - screenSizeY/2)
        #print "y:%r,yT:%r" % (y,yT)

      if gstt.X[curveNumber] == 0 and gstt.Y[curveNumber] == 0:
        x = 0
        y = 0

      newx,newy =  proj(int(x),int(y),0)


      if gstt.X[curveNumber] != 0 and gstt.Y[curveNumber] == 0:
        if 1 < len(dotsoscT[currentdotsosc[curveNumber]][curveNumber]) and newy > dotsoscT[currentdotsosc[curveNumber]][curveNumber][-1][1]:
	    #switching to the other points list queue in order to not trace the "return" laser line
	    #as we don't know how to trace that particular segment formed by that new "return" point in black
	    #destroy current queue
            dotsoscT[currentdotsosc[curveNumber]][curveNumber]=collections.deque(maxlen=nbphigh)
            currentdotsosc[curveNumber]=(currentdotsosc[curveNumber]+1)%2
            #print "Switching dotosc to #%d"%currentdotsosc
	    #creating a new one
            dotsoscT[currentdotsosc[curveNumber]][curveNumber]=collections.deque(maxlen=nbphigh)

	#we could try to let the previous queue disappear slowly…
	#instead of destroying it as stated above
	#if len(dotsoscT[(currentdotsosc+1)%2]):
	#        dotsoscT[(currentdotsosc+1)%2].popleft()
        dotsoscT[currentdotsosc[curveNumber]][curveNumber].append((newx,newy))
    	fwork.PolyLineOneColor( dotsoscT[0][curveNumber], c=colorify.rgb2hex(gstt.curveColor[curveNumber])  )
        fwork.PolyLineOneColor( dotsoscT[1][curveNumber], c=colorify.rgb2hex(gstt.curveColor[curveNumber])  )

      if gstt.X[curveNumber] == 0 and gstt.Y[curveNumber] != 0:
        if 1 < len(dotsoscT[currentdotsosc[curveNumber]][curveNumber]) and newx < dotsoscT[currentdotsosc[curveNumber]][curveNumber][-1][0]:
            dotsoscT[currentdotsosc[curveNumber]][curveNumber]=collections.deque(maxlen=nbphigh)
            currentdotsosc[curveNumber]=(currentdotsosc[curveNumber]+1)%2
            #print "Switching dotosc to #%d"%currentdotsosc
            dotsoscT[currentdotsosc[curveNumber]][curveNumber]=collections.deque(maxlen=nbphigh)

	#if len(dotsoscT[(currentdotsosc+1)%2]):
	#        dotsoscT[(currentdotsosc+1)%2].popleft()
        dotsoscT[currentdotsosc[curveNumber]][curveNumber].append((newx,newy))
    	fwork.PolyLineOneColor( dotsoscT[0][curveNumber], c=colorify.rgb2hex(gstt.curveColor[curveNumber])  )
        fwork.PolyLineOneColor( dotsoscT[1][curveNumber], c=colorify.rgb2hex(gstt.curveColor[curveNumber])  )

      #if (gstt.X == 0 and gstt.Y == 0) or (gstt.X != 0 and gstt.Y != 0):
      if (gstt.X[curveNumber] != 0 and gstt.Y[curveNumber] != 0):
        #dotsosc.append((newx,newy))
        dotsoscT[currentdotsosc[curveNumber]][curveNumber].append((newx,newy))
        #dotsoscT[0].append((newx,newy))
        #dotsoscT[1].append((newx,newy))
	#print "Plotting first lissajou curve"
	#print "gstt.X[0]=%d" % gstt.X[0]
	#print "gstt.Y[0]=%d" % gstt.Y[0]
    	fwork.PolyLineOneColor( dotsoscT[currentdotsosc[curveNumber]][curveNumber], c=colorify.rgb2hex(gstt.curveColor[curveNumber])  )

      #fwork.PolyLineOneColor( dotsoscT[0], c=colorify.rgb2hex(gstt.color)  )
      #fwork.PolyLineOneColor( dotsoscT[1], c=colorify.rgb2hex(gstt.color)  )
'''
#---------------------------------------------------------
    # ---- try to graph a second curve ----
    # There is a second sound curve that need X coordinates
    if gstt.X[1] != 0:
        if (dotsoscTa[currentdotsosca].maxlen == nbphigh and gstt.Y[1] != 0):
            print "X changing size of dotsocsTa[%d] (%d) to %d"%(currentdotsosca,dotsoscTa[currentdotsosca].maxlen,nbplow)
            dotsoscTa[currentdotsosca] = collections.deque(maxlen=nbplow)
        xTa = gstt.osc[gstt.X[1]]
        xa = 3.5 * (extracc2scrX(xTa) - screenSizeX/2)
    # Use time for X coordinates    
    else:
        if (gstt.Y[1] != 0 and dotsoscTa[currentdotsosca].maxlen == nbplow):
            print "X changing size of dotsocsTa[%d] (%d) to %d"%(currentdotsosca,dotsoscTa[currentdotsosca].maxlen,nbphigh)
            dotsoscTa[currentdotsosca] = collections.deque(maxlen=nbphigh)
        xTa = (((time.time()*50000) % 65536) - 32768)
        xa = 3.5 * (extracc2scrX(xTa) - screenSizeX/2)

    # There is a second sound curve that need Y coordinates
    if gstt.Y[1] != 0:
        if (dotsoscTa[currentdotsosca].maxlen == nbphigh and gstt.X[1] != 0):
            print "Y changing size of dotsocsTa[%d] (%d) to %d"%(currentdotsosca,dotsoscTa[currentdotsosca].maxlen,nbplow)
            dotsoscTa[currentdotsosca] = collections.deque(maxlen=nbplow)
        yTa = gstt.osc[gstt.Y[1]]
        ya = 3.5 * (extracc2scrY(yTa) - screenSizeY/2)
    else:
    # Use time for Y coordinates
        if (gstt.X[1] != 0 and dotsoscTa[currentdotsosca].maxlen == nbplow):
            print "Y changing size of dotsocsTa[%d] (%d) to %d"%(currentdotsosca,dotsoscTa[currentdotsosca].maxlen,nbphigh)
            dotsoscTa[currentdotsosca] = collections.deque(maxlen=nbphigh)
        yTa = (((time.time()*50000) % 65536) - 32768)
        ya = 3.5 * (extracc2scrY(yTa) - screenSizeY/2)

    if gstt.X[1] == 0 and gstt.Y[1] == 0:
        xa = 0
        ya = 0

    newxa,newya =  proj(int(xa),int(ya),0)


    if gstt.X[1] != 0 and gstt.Y[1] == 0:
        if 1 < len(dotsoscTa[currentdotsosca]) and newya > dotsoscTa[currentdotsosca][-1][1]:
	    #switching to the other points list queue in order to not trace the "return" laser line
	    #as we don't know how to trace that particular segment formed by that new "return" point in black
	    #destroy current queue
            dotsoscTa[currentdotsosca]=collections.deque(maxlen=nbphigh)
            currentdotsosca=(currentdotsosca+1)%2
            #print "Switching dotosc to #%d"%currentdotsosc
	    #creating a new one
            dotsoscTa[currentdotsosca]=collections.deque(maxlen=nbphigh)

	#we could try to let the previous queue disappear slowly…
	#instead of destroying it as stated above
	#if len(dotsoscTa[(currentdotsosca+1)%2]):
	#        dotsoscTa[(currentdotsosca+1)%2].popleft()
        dotsoscTa[currentdotsosca].append((newxa,newya))
    	fwork.PolyLineOneColor( dotsoscTa[0], c=colorify.rgb2hex(gstt.color)  )
        fwork.PolyLineOneColor( dotsoscTa[1], c=colorify.rgb2hex(gstt.color)  )

    if gstt.X[1] == 0 and gstt.Y[1] != 0:
        if 1 < len(dotsoscTa[currentdotsosca]) and newxa < dotsoscTa[currentdotsosca][-1][0]:
            dotsoscTa[currentdotsosca]=collections.deque(maxlen=nbphigh)
            currentdotsosca=(currentdotsosca+1)%2
            #print "Switching dotosc to #%d"%currentdotsosc
            dotsoscTa[currentdotsosca]=collections.deque(maxlen=nbphigh)

	#if len(dotsoscTa[(currentdotsosca+1)%2]):
	#        dotsoscTa[(currentdotsosca+1)%2].popleft()
        dotsoscTa[currentdotsosca].append((newxa,newya))
    	fwork.PolyLineOneColor( dotsoscTa[0], c=colorify.rgb2hex(gstt.color)  )
        fwork.PolyLineOneColor( dotsoscTa[1], c=colorify.rgb2hex(gstt.color)  )

    #if (gstt.X1 == 0 and gstt.Y1 == 0) or (gstt.X1 != 0 and gstt.Y1 != 0):
    if (gstt.X[1] != 0 and gstt.Y[1] != 0):
        #dotsosc.append((newx,newy))
        dotsoscTa[currentdotsosca].append((newxa,newya))
        #dotsoscT[0].append((newx,newy))
        #dotsoscT[1].append((newx,newy))
	#print "Plotting second lissajou curve"
	#print "gstt.X[1]=%d" % gstt.X[1]
	#print "gstt.Y[1]=%d" % gstt.Y[1]
    	fwork.PolyLineOneColor( dotsoscTa[currentdotsosca], c=colorify.rgb2hex(gstt.color)  )

    #fwork.PolyLineOneColor( dotsoscT[0], c=colorify.rgb2hex(gstt.color)  )
    #fwork.PolyLineOneColor( dotsoscT[1], c=colorify.rgb2hex(gstt.color)  )
#---------------------------------------------------------
'''


# Curve 1
def NozMode2(fwork):
    import mikuscope as mk
    dots = []
    nb_point=100


    for idx, valx in enumerate(mk.x):
            if not np.isnan(valx):
                    #print idx,valx,mk.y[idx]
                xT = valx*20000
                x = 3.5 * (extracc2scrX(xT) - 400)
                yT = mk.y[idx]*15000
                y = 3.5 * (extracc2scrY(yT) - 300)
                dots.append(proj(int(x),int(y),0))
            else:
            #dots.append(proj(0,0,0))
                fwork.PolyLineOneColor( dots, c=colorify.rgb2hex(gstt.color) )
            #dots=[]
        #if not idx%nb_point:
            #   fwork.PolyLineOneColor( dots, c=colorify.rgb2hex(gstt.color) )
    #raw_input("Hit Enter to continue")

# Curve 2
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

# Curve 3
def Orbits(fwork):

    orbits.Draw(fwork)

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

# Curve 7

def Osci(fwork):
    Pass

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
    x = x * factor + xy_center [0]
    y = - y * factor + xy_center [1]

    return x,y

