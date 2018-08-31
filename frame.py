# coding=UTF-8

'''
Created on 11 nov. 2014

@author: pclf
'''

import pygame
import gstt
import numpy as np
import math

class Frame(object):
	'''
	classdocs
	'''


	def __init__(self):
		'''
		Constructor
		'''
		
		# legacy point list
		self.point_list = []
		
		# 4 point list
		self.pl = [[],[],[],[]]
		

	def LineTo(self, xy, c, PL):
	

		self.point_list.append((xy + (c,)))				#add c to the tuple 
		self.pl[PL].append((xy + (c,)))
	
	
	def Line(self, xy1, xy2, c, PL):
		self.LineTo(xy1, 0, PL)
		self.LineTo(xy2, c , PL)
	

	def PolyLineOneColor(self, xy_list, c, PL , closed ):

		xy0 = None		
		for xy in xy_list:
			if xy0 is None:
				xy0 = xy
				#print xy0
				self.LineTo(xy0,0, PL)
			else:
				self.LineTo(xy,c, PL)
		if closed:
			self.LineTo(xy0,c, PL)
	
	def Pointransf( self, xy, xpos = 0, ypos =0, resize =1, rotx =0, roty =0 , rotz=0):

			x = xy[0] * resize
			y = xy[1] * resize
			z = 0

			rad = rotx * np.pi / 180
			cosaX = math.cos(rad)
			sinaX = math.sin(rad)

			y2 = y
			y = y2 * cosaX - z * sinaX
			z = y2 * sinaX + z * cosaX

			rad = roty * np.pi / 180
			cosaY = math.cos(rad)
			sinaY = math.sin(rad)

			z2 = z
			z = z2 * cosaY - x * sinaY
			x = z2 * sinaY + x * cosaY

			rad = rotz * np.pi / 180
			cosZ = math.cos(rad)
			sinZ = math.sin(rad)

			x2 = x
			x = x2 * cosZ - y * sinZ
			y = x2 * sinZ + y * cosZ

			#print xy, (x + xpos,y+ ypos)
			return (x + xpos,y+ ypos)
			'''
			to understand why it get negative Y
			
			# 3D to 2D projection
			factor = 4 * gstt.cc[22] / ((gstt.cc[21] * 8) + z)
			print xy, (x * factor + xpos,  - y * factor + ypos )
			return (x * factor + xpos,  - y * factor + ypos )
			'''
	
	# Send 2D point list around 0,0 with 3D rotation resizing and reposition around xpos ypos
	def rPolyLineOneColor(self, xy_list, c, PL , closed, xpos = 0, ypos =0, resize =1, rotx =0, roty =0 , rotz=0):
		xy0 = None		
		for xy in xy_list:
			if xy0 is None:
				xy0 = xy
				self.LineTo(self.Pointransf(xy0, xpos, ypos, resize, rotx, roty, rotz),0, PL)
			else:
				self.LineTo(self.Pointransf(xy, xpos, ypos, resize, rotx, roty, rotz),c, PL)
		if closed:
			self.LineTo(self.Pointransf(xy0, xpos, ypos, resize, rotx, roty, rotz),c, PL)


	def LinesPL(self, PL):

		return self.pl[PL]

	def ResetPL(self, PL):
		self.pl[PL] = []

				
	def RenderScreen(self, surface):
		if len(self.pl[gstt.simuPL]):
			xyc_prev = self.pl[gstt.simuPL][0]
			#pygame.draw.line(surface,self.black_hole_color,(x_bh_cur, y_bh_cur), (x_bh_next, y_bh_next))
			#pygame.draw.line(surface,self.spoke_color,(x_bh_cur, y_bh_cur), (x_area_cur, y_area_cur))
			for xyc in self.pl[gstt.simuPL]:
				c = int(xyc[2])
				if c: pygame.draw.line(surface,c,xyc_prev[:2],xyc[:2],3)
				xyc_prev = xyc



class FrameHolder(object):
	def __init__(self):
		self.f = None
		
