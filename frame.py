# coding=UTF-8

'''
Created on 11 nov. 2014

@author: pclf
'''

import pygame
import gstt

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
	
		#print PL
		self.point_list.append((xy + (c,)))				#add c to the tuple 
		self.pl[PL].append((xy + (c,)))

		#gstt.PL[PL].append((xy + (c,)))
		#print self.pl	
	
	
	def Line(self, xy1, xy2, c, PL):
		self.LineTo(xy1, 0, PL)
		self.LineTo(xy2, c , PL)
		return self.pl[PL]	
	
	def PolyLineOneColor(self, xy_list, c, PL , closed ):
		# code compatible avec les générateurs
		xy0 = None
		
		for xy in xy_list:
			if xy0 is None:
				xy0 = xy
				self.LineTo(xy0,0, PL)
			else:
				self.LineTo(xy,c, PL)
		if closed:
			self.LineTo(xy0,c, PL)
	
	'''
	def RenderScreen(self, surface):
		if len(self.point_list):
			xyc_prev = self.point_list[0]
			#pygame.draw.line(surface,self.black_hole_color,(x_bh_cur, y_bh_cur), (x_bh_next, y_bh_next))
			#pygame.draw.line(surface,self.spoke_color,(x_bh_cur, y_bh_cur), (x_area_cur, y_area_cur))
			for xyc in self.point_list:
				c = int(xyc[2])
				if c: pygame.draw.line(surface,c,xyc_prev[:2],xyc[:2],3)
				xyc_prev = xyc
	'''
				
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
		
