# coding=UTF-8

'''
Created on 25 nov. 2014

@author: pclf
'''
import globalVars
import itertools
import sys
import math
from globalVars import screen_size
import gstt

class Renderer(object):
	'''
	classdocs
	'''


	def __init__(self, fh):
		'''
		Constructor
		'''
		self.fh = fh

class LaserRenderer(Renderer):
	
	def __init__(self, fh, x_center, y_center, x_stretch, y_stretch, x_halfsize, y_halfsize):
		super(LaserRenderer,self).__init__(fh)
		self.x_center, self.y_center = x_center, y_center;
		self.x_stretch, self.y_stretch = x_stretch, y_stretch;
		self.x_halfsize, self.y_halfsize = x_halfsize, y_halfsize
		self.stream = self.produce()
	
	# Transformer les points écran en points laser (ToStreamPt())
	# en amont du générateur final.
	
	def genClippedLaserPts(self):
			
			# Obtenir la dernière frame valide
			f_cur = self.fh.f
			# point précédent, initialisé pour usage ultérieur
			xyrgb_prev = self.ToStreamPt((0,0,0))
			
			if f_cur is None:
				#TODO : voir si cas frame vide est mieux à traiter ici ou en aval.
				return

			for xyc in f_cur.point_list:
				xyrgb = self.ToStreamPt(xyc)
				
				#Déterminer la ligne clippée de (précédent, courant)
				#TODO : rendre configurable la zone de clipping = plage de consignes analogiques valides
				#line = ClipLine(xyrgb_prev, xyrgb, (-13000, 0), (13000, 17000))
				
				line = ClipLine(xyrgb_prev, xyrgb, (self.x_center - self.x_halfsize, self.y_center - self.y_halfsize), (self.x_center + self.x_halfsize, self.y_center + self.y_halfsize))
				# Ligne totalement en-dehors ==> on passe car il n'y a aucun point à générer
				if not line is None:
					# GENERATION OPTIONNELLE DU POINT DE DEPART :
					# s'il a été clippé, alors on réentre dans la zone de traçage et on doit
					# s'y positionner sans tracer...
					# mais c'est inutile si le point d'arrivée est "noir"
					if line[0][2] and xyc[2]:
						yield line[0][:2] + (0,0,0)
					# GENERATION POINT D'ARRIVEE :
					# quasi-systématique.
					# Seul cas d'élimination : si le point est "noir" et clippé
					# (càd on sort de la zone de traçage seulement pour se déplacer d'un point à un autre)
					if not line[1][2] or xyc[2]:
						yield line[1][:2] + xyrgb[2:]
				xyrgb_prev = xyrgb
	
	
	def produce(self):
	
		# Genere a la demande les points envoyés au laser en rajoutant des points intermédiaires
		# (compenser le temps de réponse des galvas et de la commutation des couleurs)
		
		
		while True:
		
			# point précédent, initialisé pour usage ultérieur
			xyrgb_prev = (0,0,0,0,0)
			
			#TODO : le générateur peut être vide ==> YIELDer un point bidon au minimum
			
			for xyrgb in self.genClippedLaserPts():
				
				delta_x, delta_y = xyrgb[0] - xyrgb_prev[0], xyrgb[1] - xyrgb_prev[1]
				
				#test adaptation traçage selon longueur ligne
				if math.hypot(delta_x, delta_y) < 4000:
					l_steps = [ (1.0, 8)]
				else:
					l_steps = [ (0.25, 3), (0.75, 3), (1.0, 10)]#(0.0, 1),
				for d in l_steps:
					step = d[0]
					for i in xrange(0,d[1]):
						xyrgb_step = (xyrgb_prev[0] + step*delta_x, xyrgb_prev[1] + step*delta_y) + xyrgb[2:]
						yield xyrgb_step
				
				xyrgb_prev = xyrgb
				


	def read(self, n):
	
		# Called by dac : ask ("read") for n new points needed.
		# (stream renvoie a produce dans init)
		
		d = [self.stream.next() for i in xrange(n)]
		print d
		return d
		
		
		

	def ToStreamPt(self, xyc):
		
		# compute for a given point, actual coordinates transformed by alignment parameters (center, size, zoom, axis swap,....)
		
		print ""
		print xyc
		c = xyc[2]
		XX = xyc[0] - screen_size[0]/2
		YY = xyc[1] - screen_size[1]/2
		x = (screen_size[0]/2 + ((XX * math.cos(gstt.finangle)) - (YY * math.sin(gstt.finangle))) - screen_size[0]/2) * gstt.zoomx + gstt.centerx
		y = (screen_size[1]/2 + ((XX * math.sin(gstt.finangle)) + (YY * math.cos(gstt.finangle))) - screen_size[1]/2) * gstt.zoomy + gstt.centery
		#x = (((xyc[0] * math.cos(gstt.finangle)) - (xyc[1] * math.sin(gstt.finangle))) - screen_size[0]/2) * gstt.zoomx + gstt.centerx
		#y = (((xyc[0] * math.sin(gstt.finangle)) + (xyc[1] * math.cos(gstt.finangle))) - screen_size[1]/2) * gstt.zoomy + gstt.centery
		# TODO : optimiser les calculs d'ajustement de la couleur
		print x,y
		return (x*gstt.swapx, y*gstt.swapy, ((c >> 16) & 0xFF) << 8, ((c >> 8) & 0xFF) << 8, (c & 0xFF) << 8)
	
	
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
