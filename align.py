import gstt
import frame
import pygame
import settings
import homography
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
	homography.newEDH(gstt.Laser)


def DisplayGrid(f, laser):
	l,h = screen_size
	L_SLOPE = 30
	
	f.Line((0,0),(l,0),  c=0xFFFFFF, PL=laser)
	f.LineTo((l,h),  c=0xFFFFFF, PL=laser)	
	f.LineTo((0,h),  c=0xFFFFFF, PL=laser)	
	f.LineTo((0,0),  c=0xFFFFFF, PL=laser)	

	gstt.PL[laser] = fwork.LinesPL(laser)


def Jump(fwork):
	
	if gstt.keystates[pygame.K_p]:
		DrawTestPattern(fwork)
		
	if gstt.keystates[pygame.K_x]:
		Display(fwork)
		
	if gstt.keystates[pygame.K_r]:
		gstt.centerX[gstt.Laser] -= 20
		print "r on laser ", gstt.Laser
		Display(fwork)

	if gstt.keystates[pygame.K_t]:
		gstt.centerX[gstt.Laser] += 20
		Display(fwork)
		
	if gstt.keystates[pygame.K_y]:
		gstt.centerY[gstt.Laser] -= 20
		Display(fwork)

	if gstt.keystates[pygame.K_u]:
		gstt.centerY[gstt.Laser] += 20
		Display(fwork)

	if gstt.keystates[pygame.K_f]:
		gstt.zoomX[gstt.Laser]-= 0.1
		Display(fwork)

	if gstt.keystates[pygame.K_g]:
		gstt.zoomX[gstt.Laser] += 0.1
		Display(fwork)
		
	if gstt.keystates[pygame.K_h]:
		gstt.zoomY[gstt.Laser] -= 0.1
		Display(fwork)

	if gstt.keystates[pygame.K_j]:
		gstt.zoomY[gstt.Laser] += 0.1
		Display(fwork)
	
	if gstt.keystates[pygame.K_c]:
		gstt.sizeX[gstt.Laser] -= 50
		Display(fwork)
		
	if gstt.keystates[pygame.K_v]:
		gstt.sizeX[gstt.Laser] += 50
		Display(fwork)
		
	if gstt.keystates[pygame.K_b]:
		gstt.sizeY[gstt.Laser] -= 50
		Display(fwork)
		
	if gstt.keystates[pygame.K_n]:
		gstt.sizeY[gstt.Laser] += 50
		Display(fwork)
		
	if gstt.keystates[pygame.K_l]:
		gstt.finANGLE[gstt.Laser] -= 0.001
		Display(fwork)
		
	if gstt.keystates[pygame.K_m]:
		gstt.finANGLE[gstt.Laser] += 0.001
		Display(fwork)


# Curve 0 : Warp and "windows" edit modes

''' 
 Warp edit Mode
 by default or ENTER key : 
    # Mouse : change current corner position
    # Z key : next corner


 Windows edit mode with E key from Warp edit mode
    E     : Edit mode : cycle shapes/windows 
    Z     : next corner of current shape
    ENTER : Back to Warp mode that displays all shapes.
    A     : change "Screen"

(See Readme for "windows" and shapes" concepts,..)

'''

def MappingConf(section):
    global mouse_prev, sections

    gstt.EditStep = 0
    gstt.CurrentWindow = -1
    gstt.CurrentCorner = 0
    gstt.CurrentSection = section
    mouse_prev = ((405, 325), (0, 0, 0))

    # Get all shapes points (="corners") for the given section of the conf file -> gstt.Windows 
    gstt.Windows = [] 
    sections = settings.MappingSections()

    print ""
    #print "Sections : ", sections
    print "Reading Section : ", sections[gstt.CurrentSection]

    gstt.Laser = settings.MappingRead([sections[gstt.CurrentSection],'laser'])
    print "Laser : ", gstt.Laser
    gstt.simuPL = gstt.Laser

    for Window in xrange(settings.Mapping(sections[gstt.CurrentSection])-1):
        if gstt.debug > 0:
            print "Reading option :  ", str(Window)
        shape = [sections[gstt.CurrentSection], str(Window)]
        WindowPoints = settings.MappingRead(shape)
        gstt.Windows.append(WindowPoints)

    print "Section points : " ,gstt.Windows


# ENTER : Edit warp mode
# E key : Edit windows mode 
def Mapping(fwork):
    global mouse_prev, sections

    PL = gstt.Laser
    dots = []

    #switch to edit mode Key E ?
    if gstt.keystates[pygame.K_e] and not gstt.keystates_prev[pygame.K_e] and gstt.EditStep == 0:
            print "Switching to Edit Mode"
            gstt.EditStep = 1
            gstt.CurrentWindow = 0
            gstt.CurrentCorner = 0

    # Back to Warp edit Mode if ENTER key is pressed ?
    if gstt.keystates[pygame.K_RETURN] and gstt.EditStep == 1:    
            
            print "Switching to Warp Mode"
            gstt.EditStep =0
            gstt.CurrentCorner = 0



    # Warp Display and Warp edit Mode
    # Change current corner with mouse position
    # Change corner with Z key

    if gstt.EditStep == 0:
        
        # print "Warp mode"
        # Left mouse is clicked, modify current Corner coordinate
        # print gstt.mouse

        if gstt.mouse[1][0] == mouse_prev[1][0] and mouse_prev[1][0] == 1:
            deltax = gstt.mouse[0][0]-mouse_prev[0][0]
            deltay = gstt.mouse[0][1]-mouse_prev[0][1]
            
            gstt.warpdest[gstt.Laser][gstt.CurrentCorner,0]+= (deltax *20)
            gstt.warpdest[gstt.Laser][gstt.CurrentCorner,0]+= (deltax *2)

            print "Laser ", gstt.Laser, " Corner ", gstt.CurrentCorner, "deltax ", deltax, "deltay", deltay
            print gstt.warpdest[gstt.Laser]
       
            homography.newEDH(gstt.Laser)
            settings.Write()


        # Change corner if Z key is pressed.
        if gstt.keystates[pygame.K_z] and not gstt.keystates_prev[pygame.K_z]:
            if gstt.CurrentCorner < 4:
                gstt.CurrentCorner += 1
                print "Corner : ", gstt.CurrentCorner


        # Display all windows to current PL for display
        for Window in gstt.Windows:  

            dots = []
            for corner in xrange(len(Window)):   
                #print "Editing : ", WindowPoints[corner]
                #print Window[corner][0]
                dots.append(proj(int(Window[corner][0]),int(Window[corner][1]),0))
            
            fwork.PolyLineOneColor( dots, c=colorify.rgb2hex(gstt.color), PL = PL, closed = False  )
    
        gstt.PL[PL] = fwork.LinesPL(PL)

        mouse_prev = gstt.mouse





    # EDIT WINDOWS MODE : cycle windows for current laser if press e key to adjust corner position 
    # ENTER key to warp/display mode 
    # Mouse to change current corner postion
    # Z key : next corner
    # E Key : Next window 
    # A key : Next section

    if gstt.EditStep >0:

        dots = []
        CurrentWindowPoints = gstt.Windows[gstt.CurrentWindow]

        # Draw all windows points or "corners"
        for corner in xrange(len(CurrentWindowPoints)):   
            dots.append(proj(int(CurrentWindowPoints[corner][0]),int(CurrentWindowPoints[corner][1]),0))
        fwork.PolyLineOneColor( dots, c=colorify.rgb2hex(gstt.color), PL = PL, closed = False )

        # Left mouse is clicked, modify current Corner coordinate
        if gstt.mouse[1][0] == mouse_prev[1][0] and mouse_prev[1][0] == 1:
            deltax = gstt.mouse[0][0]-mouse_prev[0][0]
            deltay = gstt.mouse[0][1]-mouse_prev[0][1]
            CurrentWindowPoints[gstt.CurrentCorner][0] += (deltax *2)
            CurrentWindowPoints[gstt.CurrentCorner][1] -= (deltay * 2)

        # Change corner if Z key is pressed.
        if gstt.keystates[pygame.K_z] and not gstt.keystates_prev[pygame.K_z]:
            if gstt.CurrentCorner < settings.Mapping(sections[gstt.CurrentSection]) - 1:
                gstt.CurrentCorner += 1
                print "Corner : ", gstt.CurrentCorner

        # E Key : Next window 
        if gstt.keystates[pygame.K_e] and not gstt.keystates_prev[pygame.K_e]:

            # Save current Window and switch to the next one.
            if gstt.CurrentWindow < settings.Mapping(sections[gstt.CurrentSection]) -1:
                print "saving "
                settings.MappingWrite(sections,str(gstt.CurrentWindow),CurrentWindowPoints)
                gstt.CurrentWindow += 1
                gstt.CurrentCorner = -1
                if gstt.CurrentWindow == settings.Mapping(sections[gstt.CurrentSection]) -1:
                    gstt.EditStep == 0
                    gstt.CurrentWindow = 0              
                print "Now Editing window ", gstt.CurrentWindow

        mouse_prev = gstt.mouse
        gstt.PL[PL] = fwork.LinesPL(PL)

    # A key : Next section ?
    if gstt.keystates[pygame.K_a] and not gstt.keystates_prev[pygame.K_a]: 
            
        print "current section : ", gstt.CurrentSection
        if gstt.CurrentSection < len(sections)-1:
            gstt.CurrentSection += 1
            print "Next section name is ", sections[gstt.CurrentSection]
            if "screen" in sections[gstt.CurrentSection]:
                print ""
                print "switching to section ", gstt.CurrentSection, " ", sections[gstt.CurrentSection]
                MappingConf(gstt.CurrentSection)
        else:
             gstt.CurrentSection = -1
        


