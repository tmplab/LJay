import gstt
import frame
import pygame
import settings
from globalVars import *

def DrawTestPattern(f):
	l,h = screen_size
	L_SLOPE = 30
	
	f.Line((0, 0), (l, 0), 0xFFFFFF, gstt.simuPL)
	f.LineTo((l, h), 0xFFFFFF, gstt.simuPL)
	f.LineTo((0, h), 0xFFFFFF, gstt.simuPL)
	f.LineTo((0, 0), 0xFFFFFF, gstt.simuPL)
	
	f.LineTo((2*L_SLOPE, h), 0, gstt.simuPL)
	for i in xrange(1,7):
		c = (0xFF0000 if i & 1 else 0) | (0xFF00 if i & 2 else 0) | (0xFF if i & 4 else 0)
		f.LineTo(((2 * i + 1) * L_SLOPE, 0), c, gstt.simuPL)
		f.LineTo(((2 * i + 2) * L_SLOPE, h), c, gstt.simuPL)
	f.Line((l*.5, h*.5), (l*.75, -h*.5), 0xFF00FF, gstt.simuPL)
	f.LineTo((l*1.5, h*.5), 0xFF00FF, gstt.simuPL)
	f.LineTo((l*.75, h*1.5), 0xFF00FF, gstt.simuPL)
	f.LineTo((l*.5, h*.5), 0xFF00FF, gstt.simuPL)


def Display(f):
	l,h = screen_size
	L_SLOPE = 30
	
	'''
	Mono laser style
	f.Line((0, 0), (l, 0), 0xFFFFFF, gstt.Laser)
	f.LineTo((l, h), 0xFFFFFF, gstt.Laser)
	f.LineTo((0, h), 0xFFFFFF, gstt.Laser)
	f.LineTo((0, 0), 0xFFFFFF, gstt.Laser)
	'''
	
	#laser = renderer.LaserRenderer(fwork_holder, gstt.centerx, gstt.centery, gstt.zoomx, gstt.zoomy, gstt.sizex, gstt.sizey)

	f.Line((0,0),(l,0),  c=0xFFFFFF, PL=gstt.Laser)
	f.LineTo((l,h),  c=0xFFFFFF, PL=gstt.Laser)	
	f.LineTo((0,h),  c=0xFFFFFF, PL=gstt.Laser)	
	f.LineTo((0,0),  c=0xFFFFFF, PL=gstt.Laser)	
	settings.Write()
	#print str(gstt.centerx) + "," + str(gstt.centery) + "," + str(gstt.zoomx) + "," + str(gstt.zoomy) + "," + str(gstt.sizex) + "," + str(gstt.sizey)



def Jump(fwork,keystates):
	
	if keystates[pygame.K_p]:
		DrawTestPattern(fwork)
		
	if keystates[pygame.K_x]:
		Display(fwork)
		
	if keystates[pygame.K_r]:
		gstt.centerX[gstt.Laser] -= 20
		Display(fwork)

	if keystates[pygame.K_t]:
		gstt.centerX[gstt.Laser] += 20
		Display(fwork)
		
	if keystates[pygame.K_y]:
		gstt.centerY[gstt.Laser] -= 20
		Display(fwork)

	if keystates[pygame.K_u]:
		gstt.centerY[gstt.Laser] += 20
		Display(fwork)

	if keystates[pygame.K_f]:
		gstt.zoomX[gstt.Laser]-= 0.1
		Display(fwork)

	if keystates[pygame.K_g]:
		gstt.zoomX[gstt.Laser] += 0.1
		Display(fwork)
		
	if keystates[pygame.K_h]:
		gstt.zoomY[gstt.Laser] -= 0.1
		Display(fwork)

	if keystates[pygame.K_j]:
		gstt.zoomY[gstt.Laser] += 0.1
		Display(fwork)
	
	if keystates[pygame.K_c]:
		gstt.sizeX[gstt.Laser] -= 50
		Display(fwork)
		
	if keystates[pygame.K_v]:
		gstt.sizeX[gstt.Laser] += 50
		Display(fwork)
		
	if keystates[pygame.K_b]:
		gstt.sizeY[gstt.Laser] -= 50
		Display(fwork)
		
	if keystates[pygame.K_n]:
		gstt.sizeY[gstt.Laser] += 50
		Display(fwork)
		
	if keystates[pygame.K_l]:
		gstt.finANGLE[gstt.Laser] -= 0.001
		Display(fwork)
		
	if keystates[pygame.K_m]:
		gstt.finANGLE[gstt.Laser] += 0.001
		Display(fwork)

