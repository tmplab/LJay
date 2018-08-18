import time
from globalVars import *
import gstt

'''
from itertools import cycle
import ConfigParser
import gstt
from jplephem.spk import SPK
from math import pi
import math


PI = pi


PL = [(200,300),(250,300)]

def points(n):

	count = 0
	for i in cycle(PL):
		if count > n:
			break	
		print n, count, i
		count += 1


points(2)


class MyParser(ConfigParser.ConfigParser):
    def as_dict(self):
        d = dict(self._sections)
        for k in d:
            d[k] = dict(self._defaults, **d[k])
            d[k].pop('__name__', None)
        return d
        
f = MyParser()
f.read("settings.conf")
d = f.as_dict()

#print d
print d['laser0']['centerx']
print d['laser1']['centerx']



def planet2screen(planetx, planety, planetz):
    screen_size = [800,600]
    a1, a2 = -1e+10,1e+10  
    b1, b2 = 0, screen_size[1]
    x = b1 + ((planetx - a1) * (b2 - b1) / (a2 - a1))
    b1, b2 = 0, screen_size[1]
    y = b1 + ((planety - a1) * (b2 - b1) / (a2 - a1))
    b1, b2 = 0, screen_size[1]
    z = b1 + ((planetz - a1) * (b2 - b1) / (a2 - a1))
    return x,y,z

def cc2range(s,min,max):
    a1, a2 = 0,127  
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
    x = x * factor + 400
    y = - y * factor + 300

    return x,y



kernel = SPK.open('de430.bsp')



year = 2018
month = 8
day = 11


JulianDate = 367 * year - 7 * (year + (month + 9)/12)/4 + 275 * month/9 + day + 1721014

print JulianDate

PlanetsPositions = []
dots = []
for planet in xrange (9):
    PlanetsPositions.append(kernel[0,planet+1].compute(JulianDate))

for planet in xrange(9):

	print ""
	print "planet ", planet
	x,y,z = planet2screen(PlanetsPositions[planet][0], PlanetsPositions[planet][1], PlanetsPositions[planet][2])
	print "x,y,z ", x,y,z
	dots.append(proj(int(x),int(y),int(z)))

print dots

t0 = time.time()
for jd in range (0,470000):
    JulianDate = jd * jd - 7 * (jd + (jd + 9)/12)/4 + 275 * jd/9 + jd + 1721014
t1 = time.time()
print ("Took %f" % (t1 - t0))
print (JulianDate)


import settings
print settings.Mapping('Windows')
print "Edit Mode"

for windows in xrange(settings.Mapping('Windows')):

    print ""
    print "Editing ", str(windows)
    shape = ['Windows', str(windows)]
    WindowPoints = settings.MappingRead(shape)

    for corner in xrange(len(WindowPoints)):   
        print "Editing : ", WindowPoints[corner]
        print "Saving point..", WindowPoints[corner]
        settings.MappingWrite(str(windows),WindowPoints)



import random
import getopt
import numpy
from numpy import linalg




def calculate(display_points,camera_points):
    """Calculates the homography if there are 4+ point pairs"""
    n = len(display_points)
    
    if n < 4:
        print 'Need 4 points to calculate transform'
        return None
        
    # This calculation is from the paper, A Plane Measuring Device
    # by A. Criminisi, I. Reid, A. Zisserman.  For more details, see:
    # http://www.robots.ox.ac.uk/~vgg/presentations/bmvc97/criminispaper/
    A = numpy.zeros((n*2,8))
    B = numpy.zeros((n*2,1))
    for i in range(0,n):
        A[2*i][0:2] = camera_points[i]
        A[2*i][2] = 1
        A[2*i][6] = -camera_points[i][0]*display_points[i][0]
        A[2*i][7] = -camera_points[i][1]*display_points[i][0]
        A[2*i+1][3:5] = camera_points[i]
        A[2*i+1][5] = 1
        A[2*i+1][6] = -camera_points[i][0]*display_points[i][1]
        A[2*i+1][7] = -camera_points[i][1]*display_points[i][1]
        B[2*i] = display_points[i][0]
        B[2*i+1] = display_points[i][1]
        
    X = linalg.lstsq(A,B)
    return numpy.reshape(numpy.vstack((X[0],[1])),(3,3))

def apply_homography(H,points):
    p = np.ones((len(points),3),'float64')
    p[:,:2] = points
    pp = np.dot(p,H.T)
    pp[:,:2]/=pp[:,2].reshape(len(p),1)
return pp[:,:2]


display_points = []
camera_points = []

ret = (0,0)
display_points.append(ret)
ret = (15,140)
display_points.append(ret)
ret = (565,137)
display_points.append(ret)
ret = (29,447)
display_points.append(ret)
ret = (560,432)

ret = (10,10)
camera_points.append(ret)
ret = (150,140)
camera_points.append(ret)
ret = (165,137)
camera_points.append(ret)
ret = (229,147)
camera_points.append(ret)
ret = (260,132)

homomap = calculate(display_points,camera_points)
newpoint = numpy.array([10, 20])

apply_homography(homomap,points)

'''

import homography
import math
import numpy as np

def EDpoint((pygamex,pygamey)):

    XX = pygamex - xy_center[0]
    YY = pygamey - xy_center[1]
    CosANGLE = math.cos(gstt.finANGLE[0])
    SinANGLE = math.sin(gstt.finANGLE[0])
    # Multilaser style
    x = (xy_center[0] + ((XX * CosANGLE) - (YY * SinANGLE)) - xy_center[0]) * gstt.zoomX[0] + gstt.centerX[0]
    y = (xy_center[1] + ((XX * SinANGLE) + (YY * CosANGLE)) - xy_center[1]) * gstt.zoomY[0] + gstt.centerY[0]
        
    return [x*1, y*1]

def test1(repetitions,points):

    t0 = time.time()

    EDpoints = []
    for point in points:
        #print point
        #print EDpoint(poin
        EDpoints.append(EDpoint(point))
    #print EDpoints

    H1 = homography.find(points1,np.array(EDpoints))
    #print "homography from 1 to 2 "
    #print H1

    for test in xrange(repetitions):
        tt = homography.apply(H1,points1)
        #print tt



    t1 = time.time()
    return t1 - t0

def test2(repetitions,points):

    t0 = time.time()


    for test in xrange(repetitions):
        tt = []
        for point in points:
            #print point
            #print EDpoint(poin

            tt.append(EDpoint(point))
        zz =np.array(tt)
        #print zz


    t1 = time.time()
    return t1 - t0

#print ""
#print 'test on '

points1 = np.array([[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200]])

#print points1

for repetitions in xrange(100):

#print ''
    #print 'homography...'


    un = test1(repetitions,points1)

#print ''
    #print 'direct...'

    deux = test2(repetitions,points1)

    '''
    if deux > un:
        pass
        print repetitions
        print un, " vs ", deux
        break
    '''

print "temps pour  ", repetitions, " : ", un, " vs ", deux
print "Par call : ", un/repetitions, " vs ", deux/repetitions
print "un / deux ", (100 * un) / deux, "%"


'''
Rotation matrices


angleX = angleX * PI / 180
angleY = angleY * PI / 180
angleZ = angleZ * PI / 180

theta = [angleX, angleY, angleZ]


def RotationMatrix(theta) :
     
    R_x = np.array([[1,         0,                  0                   ],
                    [0,         math.cos(theta[0]), -math.sin(theta[0]) ],
                    [0,         math.sin(theta[0]), math.cos(theta[0])  ]
                    ])
         
         
                     
    R_y = np.array([[math.cos(theta[1]),    0,      math.sin(theta[1])  ],
                    [0,                     1,      0                   ],
                    [-math.sin(theta[1]),   0,      math.cos(theta[1])  ]
                    ])
                 
    R_z = np.array([[math.cos(theta[2]),    -math.sin(theta[2]),    0],
                    [math.sin(theta[2]),    math.cos(theta[2]),     0],
                    [0,                     0,                      1]
                    ])
                     
                     
    R = np.dot(R_z, np.dot( R_y, R_x ))
 
    return R