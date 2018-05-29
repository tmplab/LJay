# coding=UTF-8

'''
Created on 11 nov. 2014

@author: pclf
'''

import pygame

class Frame(object):
	'''
	classdocs
	'''


	def __init__(self):
		'''
		Constructor
		'''
		self.point_list = []

	def LineTo(self, xy, c):
	   
		self.point_list.append((xy + (c,)))#add c to the tuple 
		#print (xy + (c,))
	
	
	def Line(self, xy1, xy2, c):
		self.LineTo(xy1,0)
		self.LineTo(xy2,c)
	
	def PolyLineOneColor(self, xy_list, c, closed=False):
		# code compatible avec les générateurs
		xy0 = None
		for xy in xy_list:
			if xy0 is None:
				xy0 = xy
				self.LineTo(xy0,0)
			else:
				self.LineTo(xy,c)
		if closed:
			self.LineTo(xy0,c)
	
	def RenderScreen(self, surface):
		xyc_prev = self.point_list[0]
		#pygame.draw.line(surface,self.black_hole_color,(x_bh_cur, y_bh_cur), (x_bh_next, y_bh_next))
		#pygame.draw.line(surface,self.spoke_color,(x_bh_cur, y_bh_cur), (x_area_cur, y_area_cur))
		for xyc in self.point_list:
			c = int(xyc[2])
			if c: pygame.draw.line(surface,c,xyc_prev[:2],xyc[:2],3)
			xyc_prev = xyc

class FrameHolder(object):
	def __init__(self):
		self.f = None
		