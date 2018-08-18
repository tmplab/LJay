import homography
import math
import time
from globalVars import *
import gstt
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
        print tt



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
        print zz


    t1 = time.time()
    return t1 - t0

print ""
print ""
print 'Test quand un < deux... '


# Refpoints in original coordinates
points1 = np.array([[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200],[200, -200],[200, 200],[-200, 200],[-200, -200]])


# Refpoints in pygame coordinates
#points1 = np.array([(300.0, 400.0), (500.0, 400.0), (500.0, 200.0), (300.0, 200.0), (300.0, 400.0)])
#print points1



for repetitions in xrange(2):

#print ''
    #print 'homography...'


    un = test1(repetitions,points1)

#print ''
    #print 'direct...'

    deux = test2(repetitions,points1)

    
    if deux > un:
        pass
        print repetitions, "repetitions"
        print un, " vs ", deux
        break

    

print "temps pour", repetitions, "repetitions  (ms) :", (1000*un), " vs ", (1000*deux)
print "Par call (ms) : ", (1000*un)/repetitions, " vs ", (1000*deux)/repetitions
print "un / deux ", (100 * un) / deux, "%"

print ""
repetitions = 1000
print "Test pour", repetitions,"repetitions" 


print ''
print 'Test 1 : homography...'


un = test1(repetitions,points1)
print "(ms) :", (1000*un)
print 'Test 2 : direct...'

deux = test2(repetitions,points1)

print "(ms) :", (1000*deux)
print "un / deux (%)", (100 * un) / deux