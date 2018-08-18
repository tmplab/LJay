#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# -*- mode: Python -*-

'''
LJay v0.6.2

LICENCE : CC
Sam Neurohack, pclf

'''

import globalVars
import itertools
import sys
import math
from globalVars import screen_size
import gstt
import homography

# Reference points 
Refpoints = np.array([[-200, -200],[200, -200],[200, 200],[-200, 200]])

# Store the homography for each laser.
EDH = [[], [], [], []]

newstream = OnePoint()

# Computer point in EtherDream coordinate with align corrections from proj(3Dpoints) = pygame screen coordinates
# 4 EDpoints are used to compute the homography matrix that is dramatically faster.
def EDpoint((pygamex,pygamey)):

	XX = xyc[0] - xy_center[0]
	YY = xyc[1] - xy_center[1]
	CosANGLE = math.cos(gstt.finANGLE[self.PL])
	SinANGLE = math.sin(gstt.finANGLE[self.PL])
	# Multilaser style
	x = (xy_center[0] + ((XX * CosANGLE) - (YY * SinANGLE)) - xy_center[0]) * gstt.zoomX[self.PL] + gstt.centerX[self.PL]
	y = (xy_center[1] + ((XX * SinANGLE) + (YY * CosANGLE)) - xy_center[1]) * gstt.zoomY[self.PL] + gstt.centerY[self.PL]
		
	return x*gstt.swapX[self.PL], y*gstt.swapY[self.PL]
  


# get homography from reference points and already computed EtherDream points like in .conf file.
def newEDH(EDpoints):

    EDH[gstt.Laser] = homography.find(Refpoints, np.array(EDpoints))



# compute for a given point, actual coordinates with alignment parameters (center, zoom, axis swap,..) 
# and rescaled in etherdream coord space
def EtherPoint(xyc):
	
	c = xyc[2]

	xyc[0] 
	xyc[1] 
	x,y = homography.apply(H1,np.array(xyc[0],xyc[1]))
	return (x, y, ((c >> 16) & 0xFF) << 8, ((c >> 8) & 0xFF) << 8, (c & 0xFF) << 8)



# Pull next point (in the pointlist or intermediate) in ED coordinates 
def OnePoint():
	
	while True:

		#pdb.set_trace()	
		for indexpoint,currentpoint in enumerate(PL[self.PL]):

			xyc = [currentpoint[0],currentpoint[1],currentpoint[2]]
			xyrgb = EtherPoint(xyc)

			delta_x, delta_y = xyrgb[0] - xyrgb_prev[0], xyrgb[1] - xyrgb_prev[1]
			
			#test adaptation selon longueur ligne
			if math.hypot(delta_x, delta_y) < 4000:

				l_steps = [ (1.0, 8)]

			else:
				l_steps = [ (0.25, 3), (0.75, 3), (1.0, 10)]#(0.0, 1),

			for e in l_steps:
				step = e[0]

				for i in xrange(0,e[1]):

					xyrgb_step = (xyrgb_prev[0] + step*delta_x, xyrgb_prev[1] + step*delta_y) + xyrgb[2:]		
					yield xyrgb_step

			xyrgb_prev = xyrgb
		

# Get as many points as the ED need to fill its buffer. newstream 
def GetPoints(n):

	d = [newstream.next() for i in xrange(n)]
	return d




# To be revamped....

def ClipPoint(xyc):
	# gestion simple du clipping : borner x et y, et éteindre le laser
	if xyc[0] < 0:
		xyc = (0, xyc[1], 0)
	elif xyc[0] >= screen_size[0]:
		xyc = (screen_size[0], xyc[1], 0)
	if xyc[1] < 0:
		xyc = (xyc[0], 0, 0)
	elif xyc[1] >= screen_size[1]:
		xyc = (xyc[0], screen_size[1], 0)
	return xyc

def ClipLineOneBorder(clip_line, fIsOutside, fRecalcPt):
	"""
	clippe la ligne clip_line / fonction testant sortie point + fonction de recalcul du point de clipping
	"""
	# PRINCIPE :
	# Si les 2 points sont à l'extérieur de la limite alors on quitte immédiatement
	# en prévenant l'appelant afin qu'il quitte lui aussi en éliminant la ligne clippée.
	# Si l'un des 2 points seulement est hors limite alors on le remplace par le point
	# d'intersection entre la ligne et la limite, en indiquant que ce point a été "clippé".
	# Sinon on laisse les 2 points non modifiés.
	if fIsOutside(clip_line[0]):
		if fIsOutside(clip_line[1]):
			return False
		else:
			clip_line[0] = fRecalcPt(clip_line) + (True,)
	elif fIsOutside(clip_line[1]):
		clip_line[1] = fRecalcPt(clip_line) + (True,)
		
#	print(clip_line)
	return True

def ClipLine(xy1, xy2, xy_min, xy_max):
	# Mettre les données au format où elles seront retournées
	# (càd coordonnées des points + indicateurs de clippage/modification)
	clip_line = [(xy1[:2] + (False,)), (xy2[:2] + (False,))]
	# Effectuer le traitement par rapport aux différentes bordures
	# décrivant la surface de clipping (dans notre cas un rectangle à
	# côtés horizontaux et verticaux, mais en pratique n'importe quel
	# polygone convexe pourrait convenir).
	# Abandonner tout le traitement dès que les points sont tous deux hors limite.
	# Clipper / bord gauche
	if not ClipLineOneBorder(clip_line, lambda pt: pt[0]<xy_min[0], lambda line: (
 			xy_min[0],
 			line[0][1] + (line[1][1]-line[0][1])*(xy_min[0]-line[0][0])/(line[1][0]-line[0][0]))):
		return None
	# Clipper / bord droit
	if not ClipLineOneBorder(clip_line, lambda pt: pt[0]>=xy_max[0], lambda line: (
			xy_max[0],
			line[0][1] + (line[1][1]-line[0][1])*(xy_max[0]-line[0][0])/(line[1][0]-line[0][0]))):
		return None
	# Clipper / bord haut
	if not ClipLineOneBorder(clip_line, lambda pt: pt[1]<xy_min[1], lambda line: (
			line[0][0] + (line[1][0]-line[0][0])*(xy_min[1]-line[0][1])/(line[1][1]-line[0][1]),
			xy_min[1])):
		return None
	# Clipper / bord bas
	if not ClipLineOneBorder(clip_line, lambda pt: pt[1]>=xy_max[1], lambda line: (
			line[0][0] + (line[1][0]-line[0][0])*(xy_max[1]-line[0][1])/(line[1][1]-line[0][1]),
			xy_max[1])):
		return None
	return clip_line
