
#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# -*- mode: Python -*-

'''

LJay v0.6.2

LICENCE : CC
Sam Neurohack

Homographies for align + swap corrections and warp corrections

Align + swap homography if found with 4 original points and corrected coordinates
Warp correction is disabled for the moment. Should be computed at warp edition : set 1 curve 1

Use the :

########################################################################
#  Module to compute homographies                                      #
#                                                                      #
#  Author : Alexis Mignon                                              #
#  email  : alexis.mignon@info.unicaen.fr                              #
#  date   : 10/03/2010                                                 #
########################################################################

    Module to compute homographies between two sets of 2D points
	
	implemented functions :
	 - find_homography(points1,points2) : finds the homography between 
	   two sets of 2D points
	 - find_affine_homography(points1,points2) : finds the affine 
	   homography between two sets of 2D points
	 - apply_homography(H,points) : applies homography H to the set of 
	   2D points 'points'

	example :
    >>> from homography import *
    >>> 
    >>> points1 = np.array([[ 0., 0. ],
    >>>                     [ 1., 0. ],
    >>>                     [ 0., 1. ],
    >>>                     [ 1., 1. ]])
    >>> 
    >>> points2 = np.array([[ 0.  , 0. ],
    >>>                     [ 1.  , 0. ],
    >>>                     [ 0.25, 1. ],
    >>>                     [ 0.75, 1. ]])
    >>> 
    >>> points3 = np.array([[-1., 0.],
    >>>                     [ 0.,-1.],
    >>>                     [ 0., 1.],
    >>>                     [ 1., 0.]])
    >>> 
    >>> H1 = find_homography(points1,points2)
    >>> print H1
    >>> print apply_homography(H1,points1)
    >>> H2 =  find_affine_homography(points1,points3)
    >>> print H2
    >>> print apply_homography(H2,points1)
'''


import numpy as np
import math
from scipy.linalg import svd,lstsq
import ast
import gstt
from globalVars import screen_size, xy_center

def find(points1,points2):
	if points1.shape[0] != points2.shape[0] : raise ValueError("The number of input and output points mismatches")
	if points1.shape[1] == 2 :
		p1 = np.ones((len(points1),3),'float64')
		p1[:,:2] = points1
	elif points1.shape[1] == 3 : p1 = points1
	else : raise ValueError("Bad shape for input points")
	
	if points2.shape[1] == 2 :
		p2 = np.ones((len(points2),3),'float64')
		p2[:,:2] = points2
	elif points2.shape[1] == 3 : p2 = points2
	else : raise ValueError("Bad shape for output points")
	
	npoints = len(points1)
	
	A = np.zeros((3*npoints,9),'float64')
	
	for i in xrange(npoints):
		p1i = p1[i]
		x2i,y2i,w2i = p2[i]
		xpi = x2i*p1i
		ypi = y2i*p1i
		wpi = w2i*p1i
		
		A[i*3  ,3:6] = -wpi
		A[i*3  ,6:9] =  ypi
		A[i*3+1,0:3] =  wpi
		A[i*3+1,6:9] = -xpi
		A[i*3+2,0:3] = -ypi
		A[i*3+2,3:6] =  xpi

	U,s,Vt = svd(A,full_matrices = False, overwrite_a = True)
	del U,s
	h = Vt[-1]
	H = h.reshape(3,3)
	return H

def find_affine(points1,points2):
	if points1.shape[0] != points2.shape[0] : raise ValueError("The number of input and output points mismatches")
	if points1.shape[1] == 2 :
		p1 = np.ones((len(points1),3),'float64')
		p1[:,:2] = points1
	elif points1.shape[1] == 3 : p1 = points1
	else : raise ValueError("Bad shape for input points")
	
	if points2.shape[1] == 2 :
		p2 = np.ones((len(points2),3),'float64')
		p2[:,:2] = points2
	elif points2.shape[1] == 3 : p2 = points2
	else : raise ValueError("Bad shape for output points")
	
	npoints = len(points1)
	
	A = np.zeros((3*npoints,6),'float64')
	b = np.zeros((3*npoints,1),'float64')
	for i in xrange(npoints):
		p1i = p1[i]
		x2i,y2i,w2i = p2[i]
		xpi = x2i*p1i
		ypi = y2i*p1i
		wpi = w2i*p1i
		
		A[i*3  ,3:6] = -wpi
		A[i*3+1,0:3] =  wpi
		A[i*3+2,0:3] = -ypi
		A[i*3+2,3:6] =  xpi
		
		b[i*3  ] = -y2i*p1i[2]
		b[i*3+1] =  x2i*p1i[2]

	h = lstsq(A,b,overwrite_a = True, overwrite_b = True)[0]
	H = np.zeros( (3,3) , 'float64' )
	H[:2,:] = h.reshape(2,3)
	H[2,2] = 1
	return H

def apply(H,points):
	p = np.ones((len(points),3),'float64')
	p[:,:2] = points
	pp = np.dot(p,H.T)
	pp[:,:2]/=pp[:,2].reshape(len(p),1)
	return pp[:,:2]

# Align and axis swap corrections 
# Reference points 
pointsref = np.array([(300.0, 400.0), (500.0, 400.0), (500.0, 200.0), (300.0, 200.0)])

def EDpoint(mylaser,(pygamex,pygamey)):

	XX = pygamex - xy_center[0]
	YY = pygamey - xy_center[1]
	CosANGLE = math.cos(gstt.finANGLE[mylaser])
	SinANGLE = math.sin(gstt.finANGLE[mylaser])
	# Multilaser style
	x = (-xy_center[0] + ((XX * CosANGLE) - (YY * SinANGLE)) - xy_center[0]) * gstt.zoomX[mylaser] + gstt.centerX[mylaser]
	y = (-xy_center[1] + ((XX * SinANGLE) + (YY * CosANGLE)) - xy_center[1]) * gstt.zoomY[mylaser] + gstt.centerY[mylaser]
	return [x * gstt.swapX[mylaser] , y * gstt.swapY[mylaser]]




# New total homography from always the same reference points : ED (= align + swap) transform + warp transform.
def newEDH(mylaser):

	EDpoints = []
	for point in xrange(4):
		EDpoints.append(EDpoint(mylaser,pointsref[point]))

	# H matrix tansform pygame points in Etherdream system with align and swap correction,
	H = find(pointsref, np.array(EDpoints))

	# Hwarp matrix warp etherdream points (computed with H results) 
	#Hwarp = homography.find(np.array(EDpoints), np.array(ast.literal_eval(gstt.warpdest[gstt.Laser])))

	# EDH matrix 
	gstt.EDH[mylaser] = H
	# EDH matrix with warp
	#gstt.EDH[mylaser] = np.dot(H,Hwarp)
	
	if gstt.debug >0:
		print "laser ", mylaser
		print "laser ", mylaser, "laser EDpoints :", EDpoints
		print ""
		print  "laser ", mylaser, "H :",H
		print ""
		#print  "laser ", mylaser, "warpd ",ast.literal_eval(gstt.warpdest[gstt.Laser])
		#print  "laser ", mylaser, "Hwarp ", Hwarp
		#print ""
		print  "laser ", mylaser,"new EDH :",  gstt.EDH[mylaser]
	
