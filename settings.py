#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# -*- mode: Python -*-
'''

Settings Handler

LICENCE : CC
'''

import ConfigParser
import gstt
import ast


def Write(): 

	config.set('General', 'set', str(gstt.Set))
	config.set('General', 'curve', str(gstt.Curve))
	config.set('General', 'lasernumber', str(gstt.LaserNumber))

	for i in range(gstt.LaserNumber):
		laser = 'laser' + str(i)
		config.set(laser, 'centerx', str(gstt.centerX[i]))
		config.set(laser, 'centery', str(gstt.centerY[i]))
		config.set(laser, 'zoomx', str(gstt.zoomX[i]))
		config.set(laser, 'zoomy', str(gstt.zoomY[i]))
		config.set(laser, 'sizex', str(gstt.sizeX[i]))
		config.set(laser, 'sizey', str(gstt.sizeY[i]))
		config.set(laser, 'finangle', str(gstt.finANGLE[i]))
		config.set(laser, 'swapx', str(gstt.swapX[i]))
		config.set(laser, 'swapy', str(gstt.swapY[i]))
		config.set(laser, 'warpdest', str(gstt.warpdest[i]))

	config.write(open(gstt.ConfigName,'w'))



def Read(): 
	
	gstt.Set = config.getint('General', 'set')
	gstt.Curve = config.getint('General', 'curve')
	gstt.LaserNumber = config.getint('General', 'lasernumber')

	for i in range(4):
		laser = 'laser' + str(i)
		gstt.lasersIPS[i]= config.get(laser, 'ip')
		gstt.lasersPLS[i] = config.getint(laser, 'PL')
		#gstt.lasersPLcolor[i] = config.getint(laser, 'color')
		gstt.centerX[i]= config.getint(laser, 'centerx')
		gstt.centerY[i] = config.getint(laser, 'centery')
		gstt.zoomX[i] = config.getfloat(laser, 'zoomx')
		gstt.zoomY[i] = config.getfloat(laser, 'zoomy')
		gstt.sizeX[i] = config.getint(laser, 'sizex')
		gstt.sizeY[i] = config.getint(laser, 'sizey')
		gstt.finANGLE[i] = config.getfloat(laser, 'finangle')
		gstt.swapX[i] = config.getint(laser, 'swapx')
		gstt.swapY[i] = config.getint(laser, 'swapy')
		gstt.warpdest[i]= config.get(laser, 'warpdest')



config = ConfigParser.ConfigParser()
config.read(gstt.ConfigName)


if gstt.debug > 0:
	print ""
	print "Set : ", gstt.Set
	print "Curve : ", gstt.Curve
	print "Lasers number : ", gstt.LaserNumber
	print ""
	print "Lasers parameters..."
	print "IPs ", gstt.lasersIPS
	print "PLs : ", gstt.lasersPLS
	print "center X : ", gstt.centerX
	print "center Y : ",gstt.centerY
	print "zoom X : ", gstt.zoomX
	print "zoom Y : ", gstt.zoomY
	print "size X : ", gstt.sizeX
	print "size Y : ", gstt.sizeY
	print "Rotation : ", gstt.finANGLE
	print "swap X : ", gstt.swapX
	print "swap Y : ", gstt.swapY
	print "warpdest : ", gstt.warpdest


# Save all points for a given "shape" (=['Windows','0']) shapecoord is a list 
# in any section of the mapping conf file
def MappingWrite(sections,shape, shapecoord): 

	shapestr = " ".join(str(x) for x in shapecoord)
	config.set(sections[gstt.CurrentSection], shape, shapestr.replace("] [","],["))
	config.write(open(gstt.ConfigName,'w'))


# Get a list of all points (="Corners") for a given "shape"  = [section,option] like ['Windows','0'] 
def MappingRead(shape): 
	archi = ast.literal_eval(config.get(shape[0], shape[1]))
	return archi


# Get shape numbers (i.e of windows in Windows section)
def Mapping(shape):
	return len(config.options(shape))

# Get a list of all sections
def MappingSections():
	return config.sections()
