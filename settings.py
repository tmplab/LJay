#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# -*- mode: Python -*-
'''

Settings Handler

LICENCE : CC
'''

import ConfigParser
import gstt

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

	config.write(open('settings.conf','w'))



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


config = ConfigParser.ConfigParser()
config.read("settings.conf")


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



# For Mapping()
import ast

# Save all points for a given "shape" (=['Windows','0']) shapecoord is a list.
def MappingWrite(shape, shapecoord): 

	shapestr = " ".join(str(x) for x in shapecoord)
	configmapping.set('Windows', shape, shapestr.replace("] [","],["))
	configmapping.write(open('set0.conf','w'))


# Get a list of allpoints for a given "shape" like ['Windows','0'] 
def MappingRead(shape): 

	#print shape[0], shape[1]
	#print configmapping.get(shape[0], shape[1])
	archi = ast.literal_eval(configmapping.get(shape[0], shape[1]))
	return archi


# Get shape numbers (of windows in Windows section)
def Mapping(shape):
	return len(configmapping.options(shape))

def MappingSections():
	return configmapping.sections()


configmapping = ConfigParser.ConfigParser()
configmapping.read("set0.conf")

