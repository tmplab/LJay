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
'''
import homography
import math
import numpy as np


pl = 0
color = -1
ip = '192.168.1.5'
centerx = 0
centery = 0
zoomx = 15.0
zoomy = 15.0
sizex = 32000
sizey = 32000
finangle = 0.0
swapx = 1
swapy = 1

print xy_center

def EDpoint((pygamex,pygamey)):

    XX = pygamex - xy_center[0]
    YY = pygamey - xy_center[1]
    CosANGLE = math.cos(finangle)
    SinANGLE = math.sin(finangle)
    # Multilaser style
    x = (xy_center[0] + ((XX * CosANGLE) - (YY * SinANGLE)) - xy_center[0]) * zoomx + centerx
    y = (xy_center[1] + ((XX * SinANGLE) + (YY * CosANGLE)) - xy_center[1]) * zoomy + centery
        
    return [x*1, y*1]


# Reference points 
pointsref = np.array([(300.0, 400.0), (500.0, 400.0), (500.0, 200.0), (300.0, 200.0)])

# Store the homography for each laser.
EDH = [[], [], [], []]


# New total homography from always the same reference points : ED transform + warp transform.
def newEDH():

    print "pointsref : ",pointsref

    EDpoints = []
    for point in xrange(4):
        EDpoints.append(EDpoint(pointsref[point]))
    print ""
    print "EDpoints :", EDpoints
   

    # H matrix tansform pygame points in Etherdream system with geometric correctio,
    H = homography.find(pointsref, np.array(EDpoints))
    print ""
    print "H :",H

    # Hwarp matrix warp etherdream points (computed with H) 
    Hwarp = homography.find(np.array(EDpoints), np.array(gstt.warpdest[gstt.Laser]))
    print ""
    print "warpdest : ", type(gstt.warpdest[gstt.Laser])
    print  np.array(gstt.warpdest[gstt.Laser])
    print "Hwarp ", Hwarp
    
    
    # EDH matrix 
    EDH[gstt.Laser] = np.dot(H,Hwarp)

    print ""
    EDH[gstt.Laser] = H
    print "new EDH :",  EDH[gstt.Laser]


newEDH()

final = homography.apply(EDH[gstt.Laser],np.array([(300.0, 400.0)]))
print final

'''
'''
for test in xrange(repetitions):
    tt = homography.apply(H1,points1)
    #print tt


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
'''
import redis
from multiprocessing import Process, Queue, TimeoutError 
import random, ast
import settings
settings.Read()
import newdacp
import homography

gstt.debug = 2


def dac_process(number, pl):
    while True:
        try:
            d = newdacp.DAC(number,pl)
            d.play_stream()
        except Exception as e:

            import sys, traceback
            if gstt.debug == 2:
                print '\n---------------------'
                print 'Exception: %s' % e
                print '- - - - - - - - - - -'
                traceback.print_tb(sys.exc_info()[2])
                print "\n"
            pass

        except KeyboardInterrupt:
            sys.exit(0)
 


if __name__ == '__main__':

        
    r = redis.StrictRedis(host=gstt.LjayServerIP , port=6379, db=0)

    grid_points = [(300.0+random.randint(-100, 100), 200.0+random.randint(-100, 100), 0), (500.0+random.randint(-100, 100), 200.0+random.randint(-100, 100), 65280), (500.0+random.randint(-100, 100), 400.0+random.randint(-100, 100), 65280), (300.0+random.randint(-100, 100), 400.0+random.randint(-100, 100), 65280), (300.0+random.randint(-100, 100), 200.0+random.randint(-100, 100), 65280)]
    if r.set('/pl/0', grid_points) == True:
        print "original /pl/0 ", ast.literal_eval(r.get('/pl/0'))

    grid_points = [(300.0+random.randint(-100, 100), 200.0+random.randint(-100, 100), 0), (500.0+random.randint(-100, 100), 200.0+random.randint(-100, 100), 65280), (500.0+random.randint(-100, 100), 400.0+random.randint(-100, 100), 65280), (300.0+random.randint(-100, 100), 400.0+random.randint(-100, 100), 65280), (300.0+random.randint(-100, 100), 200.0+random.randint(-100, 100), 65280)]
    if r.set('/pl/1', grid_points) == True:
        print "original /pl/1 ", ast.literal_eval(r.get('/pl/1'))

    grid_points = [(300.0+random.randint(-100, 100), 200.0+random.randint(-100, 100), 0), (500.0+random.randint(-100, 100), 200.0+random.randint(-100, 100), 65280), (500.0+random.randint(-100, 100), 400.0+random.randint(-100, 100), 65280), (300.0+random.randint(-100, 100), 400.0+random.randint(-100, 100), 65280), (300.0+random.randint(-100, 100), 200.0+random.randint(-100, 100), 65280)]
    if r.set('/pl/2', grid_points) == True:
        print "original /pl/2 ", ast.literal_eval(r.get('/pl/2'))

    dac_worker0= Process(target=dac_process,args=(0,0))
    dac_worker0.start()
    
    dac_worker1= Process(target=dac_process,args=(1,0))
    dac_worker1.start()

    dac_worker2= Process(target=dac_process,args=(2,0))
    dac_worker2.start()
    
    try:
        while True:
            #print "lstt0 : ", r.get('lstt0')
        
            zrr = random.randint(0, 100000)
            #print zrr
            if zrr == 98:
                #print 'ZRR = 98'
                grid_points = [(300.0+random.randint(-100, 100), 200.0+random.randint(-100, 100), 0), (500.0+random.randint(-100, 100), 200.0+random.randint(-100, 100), 65280), (500.0+random.randint(-100, 100), 400.0+random.randint(-100, 100), 65280), (300.0+random.randint(-100, 100), 400.0+random.randint(-100, 100), 65280), (300.0+random.randint(-100, 100), 200.0+random.randint(-100, 100), 65280)]
                #print "0", grid_points
                r.set('/pl/0', grid_points)

                grid_points = [(300.0+random.randint(-100, 100), 200.0+random.randint(-100, 100), 0), (500.0+random.randint(-100, 100), 200.0+random.randint(-100, 100), 65280), (500.0+random.randint(-100, 100), 400.0+random.randint(-100, 100), 65280), (300.0+random.randint(-100, 100), 400.0+random.randint(-100, 100), 65280), (300.0+random.randint(-100, 100), 200.0+random.randint(-100, 100), 65280)]
                #print "1", grid_points
                r.set('/pl/1', grid_points)

                grid_points = [(300.0+random.randint(-100, 100), 200.0+random.randint(-100, 100), 0), (500.0+random.randint(-100, 100), 200.0+random.randint(-100, 100), 65280), (500.0+random.randint(-100, 100), 400.0+random.randint(-100, 100), 65280), (300.0+random.randint(-100, 100), 400.0+random.randint(-100, 100), 65280), (300.0+random.randint(-100, 100), 200.0+random.randint(-100, 100), 65280)]
                #print "2", grid_points
                r.set('/pl/2', grid_points)
            
            #print grid_points
            #if r.set('pl0', grid_points) == True:
                #print "pl0 ", ast.literal_eval(r.get('pl0'))
 
    except KeyboardInterrupt:
        pass
    finally:

        dac_worker0.join()
        dac_worker1.join()
        dac_worker2.join()
 
    print "Fin des haricots"