#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
"""
LJay/LJ 

v0.7.0

DMX Handler 

import mydmx
mydmx.send(channel, value)

by Sam Neurohack and llstr 
from /team/laser

"""
import pysimpledmx
import sys
from serial.tools import list_ports
import serial,time
from threading import Thread
import gstt
from sys import platform


gstt.serdmx =""
print("")
print("")
print("Searching for DMX serial devices...")
ports = list(list_ports.comports())
for p in ports:
    print(p)

try:

    # Find serial port
    if  platform == 'darwin':
        gstt.serdmx = next(list_ports.grep("DMX USB PRO"))
        print "darwin OS"
    if  platform == 'linux2':
        print "Linux OS"
        gstt.serdmx = next(list_ports.grep("/dev/ttyUSB0"))
    print ("Serial Picked for DMX : ",gstt.serdmx[0])

    if gstt.serdmx != "":
        mydmx = pysimpledmx.DMXConnection(gstt.serdmx[0])

    # thread to code if DMX read
    '''
    thread = Thread(target=DMXinProcess, args=())
    thread.setDaemon(True)
    thread.start()
    '''

    
except StopIteration:
    print ("No DMX device found")


def send(channel, value):

    if gstt.serdmx != "":
        #mydmx.setChannel((channel + 1 ), value, autorender=True)
        # calling render() is better more reliable to actually sending data
        
        # Some strange bug. Need to add one to required dmx channel is done automatically
        mydmx.setChannel((channel + 1 ), value)
        mydmx.render()
        print "Sending DMX Channel : ", str(channel), " value : ", str(value)

if gstt.serdmx != "":
    send(8,180)#change tilt to 180° (see http://static.boomtonedj.com/pdf/manual/43/43105_manuelfroggyledrgbw.pdf)


#send(3,[0,255] vary red from 0 to 255
