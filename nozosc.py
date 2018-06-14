#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# -*- mode: Python -*-

# Le joystick bougé envoie automatiquement des messages knobs 30 et 31
# Protocole sur le port série :

# Au debut ca envoie rien.

# FF arrête tous les envois en cours
# A0 a AC  Les trucs qui oscillent 
# 0 à 31 les knobs : 2 messages FF numeroknob 00 FF
# N'importe quelle autre valeur va arrêter un 
# F0 Donne le type de nozoid  "MMO3" : FF F0 4D 33
# F1 ralenti
# F2 accélère
# 

import random
import pysimpledmx
import sys
from serial.tools import list_ports
import serial,time
from threading import Thread
import gstt,socket
import struct
from OSC import OSCServer, OSCClient, OSCMessage
import types
from sys import platform
import argparse

tLfoVal0 =  [0] * 256
tLfoVal1 =  [0] * 256
tLfoDelta = [0] * 256

lfoval0=0
lfoval1=0

argsparser = argparse.ArgumentParser(description="nozosc.py is an OSC Server between nozoïd devices and LJay.py/bhorosc.py server")
argsparser.add_argument("-i","--iport",help="Port number receiving OSC commands (8003 by default)",type=int)
argsparser.add_argument("-o","--oport",help="Port number sending OSC commands to LJay (bhorosc.py) (8001 by default)",type=int)
argsparser.add_argument("-n","--nozport",help="Serial port number connected to Nozoïd USB ((ACM)0 by default)",type=int)
args = argsparser.parse_args()

if args.iport:
        iport=args.iport
else:
        iport=gstt.noziport

if args.oport:
        oport=args.oport
else:
        oport=gstt.nozoport

if args.nozport:
        nozport=args.nozport
else:
        nozport=gstt.nozuport

#DMX
def senddmx0():
    for channel in range (1,512):
	senddmx(channel,0)

def senddmx(channel, value):

    if gstt.serdmx != "":
        #mydmx.setChannel((channel + 1 ), value, autorender=True)
        # calling render() is better more reliable to actually sending data

        # Some strange bug. Need to add one to required dmx channel is done automatically
        mydmx.setChannel((channel + 1 ), value)
        mydmx.render()
        print "Sending DMX Channel : ", str(channel), " value : ", str(value)



#oscIPin = "192.168.42.194"
#oscIPin = "127.0.0.1"
oscIPin = socket.gethostbyname(socket.gethostname())
#oscPORTin = 8003
oscPORTin = iport
oscpathin = ""

#oscIPout = ""
#oscIPout = "10.255.255.194"
oscIPout = socket.gethostbyname(socket.gethostname())
#bhorosc.py
#oscPORTout = 8001
oscPORTout = oport
#oscPORTout = 8002

oscdevice = 0

NozMsg=[0,0,0,0]
NozMsgL=[0,0,0,0,0,0]

print("")
print("OSCServer")
print ("M controller is receiving on ", oscIPin, ":",str(oscPORTin))
#oscserver = OSCServer( ("192.168.42.194", 8001) )
oscserver = OSCServer( (oscIPin, oscPORTin) )
oscserver.timeout = 0
OSCRunning = True
print oscserver.address()


def handle_timeout(self):
    self.timed_out = True


def twoDigit( number ):
   return '%02d' % number

def twoDigitHex( number ):
   return '%02x' % number
   
def send(channel):
    Mser.write([channel]) 
    
def XXXNozMsg(channel,value):
    
    print channel
    print value
    
    
#
# OSC messages handlers
#
   
oscserver.handle_timeout = types.MethodType(handle_timeout, oscserver)


osclient = OSCClient()
osclientme = OSCClient()
oscmsg = OSCMessage()

#oscaddress="/on"

# sendosc(oscaddress, [arg1, arg2,...])

def sendosc(oscaddress,oscargs):
#def sendosc(oscargs):
    
    # also works : osclient.send(OSCMessage("/led", oscargs))

    oscpath = oscaddress.split("/")
    pathlength = len(oscpath)

    oscmsg = OSCMessage()

    if oscpath[2] == "name":
	print "we are asked to send a name"
	oscmsg.setAddress(oscaddress)
	oscmsg.append(oscargs)

    if oscpath[2] == "status":
	print "we are asked to send a status"
	oscmsg.setAddress(oscaddress)
	oscmsg.append(oscargs)

    if oscpath[2] == "knob":
	print "we are asked to send knob %d's value" % int(oscargs[0:2])
	oscmsg.setAddress(''.join((oscaddress,"/",str(int(oscargs[0:2])))))
	oscmsg.append(int(oscargs[2:100]))
	
    if oscpath[2] == "osc":
	#print "we are asked to send continusouly an osc value"
	#print oscargs
	oscmsg.setAddress(''.join((oscaddress,"/",str(int(oscargs[0:2])))))
	oscmsg.append(int(oscargs[2:100]))

    if oscpath[2] == "lfo":
	#print "we are asked to send continusouly a lfo value"
	oscmsg.setAddress(''.join((oscaddress,"/",str(int(oscargs[0:2])))))
	oscmsg.append(int(oscargs[2:100]))

    if oscpath[2] == "vco":
	#print "we are asked to send continusouly a vco value"
	oscmsg.setAddress(''.join((oscaddress,"/",str(int(oscargs[0:2])))))
	oscmsg.append(int(oscargs[2:100]))

    if oscpath[2] == "mix":
	#print "we are asked to send continusouly a mix value"
	oscmsg.setAddress(''.join((oscaddress,"/",str(int(oscargs[0:2])))))
	oscmsg.append(int(oscargs[2:100]))

    if oscpath[2] == "X":
	print "we are asked to send continusouly a X value"
	oscmsg.setAddress(oscaddress)
	oscmsg.append(oscargs)

    if oscpath[2] == "Y":
	print "we are asked to send continusouly a Y value"
	oscmsg.setAddress(oscaddress)
	oscmsg.append(oscargs)

    if oscpath[2] == "offset":
	print "we are asked to offset a curve"
	oscmsg.setAddress(oscaddress)
	oscmsg.append(oscargs)

    if oscpath[2] == "color":
	#print "we are asked to change lazer color"
	oscmsg.setAddress(oscaddress)
	if len(oscargs) > 0:
		oscmsg.append(oscargs)

    try:
	osclient.sendto(oscmsg, (oscIPout, oscPORTout))
	oscmsg.clearData()
    except:
	print ('Connection refused at ',oscIPout)
        pass

# sendme(oscaddress, [arg1, arg2,...])
osclientme.connect((oscIPin, oscPORTin)) 

def sendme(oscaddress,oscargs):
#def sendme(oscargs):
        
    oscmsg = OSCMessage()
    oscmsg.setAddress(oscaddress)
    oscmsg.append(oscargs)
    
    #print "sending me: ",oscmsg, oscargs
    try:
        osclientme.sendto(oscmsg, (oscIPin, oscPORTin))
        oscmsg.clearData()
    except:
        print ('Connection to mycontroller refused')
        pass
    #time.sleep(0.001)
  
  
  
# RAW OSC Frame available ? 
def osc_frame():

    # clear timed_out flag
    #print "frame"
    oscserver.timed_out = False
    # handle all pending requests then return
    
    while not oscserver.timed_out:
        oscserver.handle_request()

    #time.sleep(0.0001)

    
#
# OSC messages handlers
#
   
# default handler 
def nozhandler(path, tags, args, source):

	
	oscpath = path.split("/")
	pathlength = len(oscpath)
	print ""
	print "default handler"
	print "path:",path,"pathlength:", pathlength,"oscpath:", oscpath,"args:", args

	# /cc/number value
	if oscpath[1] == "cc" :
		number = int(oscpath[2])
		value = int(args[0])
		gstt.cc[number] = value    



# /on
def nozon(path, tags, args, source):
    global oscIPout,oscdevice,controlmatrix

    user = ''.join(path.split("/"))
    #print "New OSC Client : " + str(source[0])
    oscIPout = str(source[0])
    osclient.connect((oscIPout, oscPORTout))
    print ("Sending on ", oscIPout, ":",str(oscPORTout))
    status("NozOSC ON")
    print ("Stop Com from Nozoid")
    Mser.write([0xFF])
    print ("asking for with nozoid type...")
    Mser.write([0xF0])

# /stop
def nozstop(path, tags, args, source):

    print ("Stop Com from Nozoid")
    for curve in range(0, gstt.maxCurvesByLaser):
	print "Resetting Curve[%d]"%curve
    	sendosc("/nozoid/X", [0x00,curve])
	sendosc("/nozoid/Y", [0x00,curve])
	gstt.X[curve]=0
	gstt.Y[curve]=0

    Mser.write([0xFF]) 
#    time.sleep(1)
    print "In_Waiting garbage msg # after 0xFF sent:",Mser.in_waiting
#    time.sleep(1)

    while Mser.in_waiting != 0:
        print "Still",Mser.in_waiting,"In_Waiting garbage msg after 0xFF sent"
	Mser.read()

# /name 
def nozname(path, tags, args, source):

    print ("asking for my nozoid name...")
    Mser.write([0xF0])

    
# /lfo
def nozlfo(path, tags, args, source):
	#print "LFO"
	#print "P:",path,",T:",tags,",A:",args,",S:",source
	print ("LFO ", args[0], "asked")
	Mser.write([0xA2 + int(args[0])]) # 0xA3 : LFO 1 / 0xA4 : LFO 2  / 0xA5 : LFO 3 


# /osc
def nozosc(path, tags, args, source):
	#print "OSC"
	print ("OSC ", args[0], "asked")
	Mser.write([0x9F + int(args[0])]) # 0xA0 : OSC 1 / 0xA1 : OSC 2  / 0xA2 : OSC 3 

# /vco
def nozvco(path, tags, args, source):
	#print "OSC"
	print ("VCO ", args[0], "asked")
	Mser.write([0xF2 + int(args[0])]) # 0xA0 : OSC 1 / 0xA1 : OSC 2  / 0xA2 : OSC 3

# /mix
def nozmix(path, tags, args, source):
	#print "OSC"
	print ("MIX ", args[0], "asked")
	Mser.write([0xF5 + int(args[0])]) # 0xA0 : OSC 1 / 0xA1 : OSC 2  / 0xA2 : OSC 3

# /down
def nozdown(path, tags, args, source):
	#print ("UP ", args[0], "asked")
	#print "Path:",path,",Tags:",tags,",Args:",args,",Source:",source
	if args:
		Mser.write([0xF1,int(args[0])]) # 0xF1 slowing down flow with argument
	else:
		Mser.write([0xF1]) # 0xF1 slowing down flow

# /up
def nozup(path, tags, args, source):
	if args:
		Mser.write([0xF2,int(args[0])]) # 0xF2 speeding up with argument
	else:
		Mser.write([0xF2]) # 0xF2 speeding up flow

# /knob
def nozknob(path, tags, args, source):
	print ("KNOB", args[0], "asked")
	Mser.write([0 + int(args[0])]) # 0xA0 : OSC 1l / 0xA1 : OSC 2  / 0xA2 : OSC 3 

# /nozoid/offset value = decalage X, decalage Y, courbe
def nozoffset(path, tags, args, source):
    print "Here we are in /nozoid/offset in nozosc"
    offsetX = int(args[0])
    offsetY = int(args[1])
    curveNumber = int(args[2])
    print "offsetX=%d,offsetY=%d,curveNumber=%d"%(offsetX,offsetY,curveNumber)
    sendosc("/nozoid/offset",[offsetX,offsetY,curveNumber])

# /X change sound curve to draw on X axis and tell nozoids to send this sound curve
def nozX(path, tags, args, source):
	#print args
	if 0 == len(args):
		for CurveNumber in range(0, gstt.maxCurvesByLaser):
			print "CurveNumber %d X is tracing osc %d" %(CurveNumber,gstt.X[CurveNumber])
	if 2 == len (args):
		print "Oh! You are setting a curve number as second argument?! It's so cute!"
		CurveNumber = args[1]
		print "CurveNumber",CurveNumber
	else:
		CurveNumber = 0

	if 0 < len(args):
	  print "Setting active X[%d] trace to %d" %(CurveNumber,args[0])
	  #print type(args[0])
	  #deactivate currently active osc used
	  if gstt.X[CurveNumber] <= 16:
		Mser.write([0x9F + gstt.X[CurveNumber]])
	  else:
		Mser.write([0xE2 + gstt.X[CurveNumber]])

	  if args[0] <= 16:
		Mser.write([0x9F + int(args[0])])
		print("/nozoid/X/%d") % (0x00 + int(args[0]))
		sendosc("/nozoid/X",[(0x00 + int(args[0])),CurveNumber])
	  else:
		Mser.write([0xE2 + int(args[0])])
		print("/nozoid/X/%d") % (0x43 + int(args[0]))
		sendosc("/nozoid/X",[(0x43 + int(args[0])),CurveNumber])

	  gstt.X[CurveNumber]=int(args[0])

# /Y
# change sound curve to draw on Y axis and tell nozoids to send this sound curve

def nozY(path, tags, args, source):
	#print args
	if 0 == len(args):
		for CurveNumber in range(0, gstt.maxCurvesByLaser):
			print "CurveNumber %d Y is tracing osc %d" %(CurveNumber,gstt.Y[CurveNumber])
	if 2 == len (args):
		print "Oh! You are setting a curve number as second argument?! It's so fine!"
		CurveNumber = args[1]
		print "CurveNumber",CurveNumber
	else:
		CurveNumber = 0

	if 0 < len(args):
	  #print "Args len %d" % len(args)
	  print "Setting active Y[%d] trace to %d" %(CurveNumber,args[0])
	  #print type(args[0])
	  #deactivate currently active osc sent by nozoid saved into gstt.Y at previous call
	  #even if it's the same which will be asked again…
	  if gstt.Y[CurveNumber] <= 16:
		Mser.write([0x9F + gstt.Y[CurveNumber]])
	  else:
		Mser.write([0xE2 + gstt.Y[CurveNumber]])

	  if args[0] <= 16:
		Mser.write([0x9F + int(args[0])])
		print("/nozoid/Y/%d") % (0x00 + int(args[0]))
		sendosc("/nozoid/Y",[(0x00 + int(args[0])),CurveNumber])
	  else:
		Mser.write([0xE2 + int(args[0])])
        	print("/nozoid/Y/%d") % (0x43 + int(args[0]))
		sendosc("/nozoid/Y",[(0x43 + int(args[0])),CurveNumber])

	  gstt.Y[CurveNumber]=int(args[0])

def nozcolor(path, tags, args, source):
	#print "Quelqu'un (je ne sais pas qui) m'a demandé de la couleur…"
        #print "args",args
        if len(args) <= 1:
          if len(args) == 0:
            curveNumber = 0
          if len(args) == 1:
            curveNumber = int(args[0])
	  sendosc("/nozoid/color",args)
	  print "Hum maybe you should see now what bhorosc.py has answered about colorZ"


        else:
          if len(args) > 3:
            curveNumber = int(args[3])
          else:
            curveNumber = 0
          print "Changing Curve[%d]'s color to R:%d G:%d B:%d" % (curveNumber,args[0], args[1], args[2])
          gstt.curveColor[curveNumber][0]=int(args[0])
          gstt.curveColor[curveNumber][1]=int(args[1])
          gstt.curveColor[curveNumber][2]=int(args[2])
	  sendosc("/nozoid/color",[int(args[0]),int(args[1]),int(args[2]),int(args[3])])


def flashdmx(path, tags, args, source):

	for channel in range (1,10):
		vrand=random.randint(0,255)
		senddmx(channel,vrand)

	for channel in range (21,30):
		vrand=random.randint(0,255)
		senddmx(channel,vrand)

	for channel in range (41,44):
		vrand=random.randint(0,255)
		senddmx(channel,vrand)

# Send text to status display widget
def nozstatus(path, tags, args, source):
    sendosc("/nozoid/status", args[0])

# registering all OSC message handlers

oscserver.addMsgHandler( "/nozoid/on", nozon )
oscserver.addMsgHandler( "/nozoid/stop", nozstop )
oscserver.addMsgHandler( "default", nozhandler )
oscserver.addMsgHandler( "/nozoid/name", nozname )
oscserver.addMsgHandler( "/nozoid/lfo", nozlfo )
oscserver.addMsgHandler( "/nozoid/osc", nozosc )
oscserver.addMsgHandler( "/nozoid/vco", nozvco )
oscserver.addMsgHandler( "/nozoid/mix", nozmix )
oscserver.addMsgHandler( "/nozoid/up", nozup )
oscserver.addMsgHandler( "/nozoid/down", nozdown )
oscserver.addMsgHandler( "/nozoid/knob", nozknob )
oscserver.addMsgHandler( "/nozoid/status", nozstatus )
oscserver.addMsgHandler( "/nozoid/X", nozX )
oscserver.addMsgHandler( "/nozoid/Y", nozY )
oscserver.addMsgHandler( "/nozoid/color", nozcolor )
oscserver.addMsgHandler( "/nozoid/flashdmx", flashdmx )
oscserver.addMsgHandler( "/nozoid/offset", nozoffset )


#
# Running...
#
    
        
# Search for nozoid

print("")
print("Available serial devices")
ports = list(list_ports.comports())
for p in ports:
    print(p)

#raw_input("Will try to select Last Serial Port\nPress Enter to continue...")

try:

    # Find nozoid serial port
    if  platform == 'darwin':
        sernozoid = next(list_ports.grep("Arduino Due"))
    if  platform == 'linux2':
        #print "ACM"+str(nozport)
        sernozoid = next(list_ports.grep("ACM"+str(nozport)))



    print "Serial Picked for Nozoid :",sernozoid[0]
    Mser = serial.Serial(sernozoid[0],115200)
    #Mser = serial.Serial(gstt.sernozoid[0],115200,timeout=5)
    print "Serial connection..."
    print "Device..." 
    print(Mser.is_open)

	# Serial port sync
    print "In_Waiting garbage msg # at the serial opening:",Mser.in_waiting
    
    while Mser.in_waiting != 0:
        print "Still",Mser.in_waiting,"In_Waiting msg to flush at the opening"
        Mser.read()

    #sendme("/stop",1)
    #sendme("/on",1)

    # infinite loop display Nozoid message
    # Todo transfer to a separate thread.
    Mser.write([0xFF])

    #print ("asking for with nozoid type...")
    #the serial way please
    Mser.write([0xF0])
    #or the OSC way please !
    sendme("/nozoid/name","")

except StopIteration:
    print ("No Nozoid device found")
    Mser = False
    
if Mser != False:
    pass

    try:
    # Find DMX serial port
	if  platform == 'darwin':
		gstt.serdmx = next(list_ports.grep("DMX USB PRO"))
	if  platform == 'linux2':
		gstt.serdmx = next(list_ports.grep("/dev/ttyUSB0"))

	#print "gstt.serdmx", gstt.serdmx
	#raw_input("Press Enter to continue...")

	continueprint ("Serial Picked for DMX : ",gstt.serdmx[0])

	if gstt.serdmx != "":
		mydmx = pysimpledmx.DMXConnection(gstt.serdmx[0])

	senddmx0()
	time.sleep(1)

	vrand=random.randint(0,255)
	senddmx(1,vrand)#dimmer full
	vrand=random.randint(0,255)
	senddmx(3,vrand)#red
	vrand=random.randint(0,255)
	senddmx(4,vrand)#green
	vrand=random.randint(0,255)
	senddmx(5,vrand)#blue
	vrand=random.randint(0,255)
	senddmx(6,vrand)#
	vrand=random.randint(0,255)
	senddmx(7,vrand)#pan
	vrand=random.randint(0,255)
	senddmx(8,vrand)#change tilt to 180° (see http://static.boomtonedj.com/pdf/manual/43/43105_manuelfroggyledrgbw.pdf)
	vrand=random.randint(0,255)
	senddmx(9,vrand)#rotation speed

	vrand=random.randint(0,255)
	senddmx(21,vrand)
	vrand=random.randint(0,255)
	senddmx(22,0)
	vrand=random.randint(0,255)
	senddmx(23,vrand)
	vrand=random.randint(0,255)
	senddmx(24,0)
	vrand=random.randint(0,255)
	senddmx(25,0)
	vrand=random.randint(0,255)
	senddmx(26,255)
	vrand=random.randint(0,255)
	senddmx(27,255)
	vrand=random.randint(0,255)
	senddmx(28,255)
	vrand=random.randint(0,255)
	senddmx(29,255)
	vrand=random.randint(0,255)
#    senddmx(30,vrand)
	vrand=random.randint(0,255)
#    senddmx(31,vrand)
	vrand=random.randint(0,255)
#    senddmx(32,0)
	vrand=random.randint(0,255)
#    senddmx(33,vrand)

	vrand=random.randint(0,255)
	senddmx(41,vrand)
	vrand=random.randint(0,255)
	senddmx(42,vrand)
	vrand=random.randint(0,255)
	senddmx(43,vrand)

	vrand=random.randint(0,255)
#    senddmx(44,255)
	vrand=random.randint(0,255)
#    senddmx(45,255)
	vrand=random.randint(0,255)
#    senddmx(46,vrand)
	vrand=random.randint(0,255)
#    senddmx(47,vrand)
	vrand=random.randint(0,255)

    except StopIteration:
	    print ("No DMX device found")
	    mydmx = False
    if mydmx != False:
	pass
#end DMX exception initialization
#mydmx is *set* to false so can be checked for the following…

    while True:

        #print "loop"
        osc_frame()

	if Mser.in_waiting != 0:        
         NozMsg = Mser.read(4)

         if ord(NozMsg[1]) < 160:
            (val,) = struct.unpack_from('>H', NozMsg, 2)
            sendosc("/nozoid/knob",''.join((twoDigit(ord(NozMsg[1])),str(val))))
        
         if ord(NozMsg[1]) >= 0xA0 and ord(NozMsg[1]) < 0xF0:

	    OrdNozMsg=ord(NozMsg[1])

	    tLfoVal0[OrdNozMsg]=tLfoVal1[OrdNozMsg]

            (val,) = struct.unpack_from('>h', NozMsg, 2)

	    tLfoVal1[OrdNozMsg]=val
	    tLfoDelta[OrdNozMsg]=abs(tLfoVal1[OrdNozMsg]-tLfoVal0[OrdNozMsg])

	    #print "delta lfo %x : %d" % (OrdNozMsg, tLfoDelta[OrdNozMsg])

            sendosc("/nozoid/osc",''.join((twoDigit(ord(NozMsg[1])-0x9F),str(val))))

         if ord(NozMsg[1]) == 0xF0:   
	    print ''.join((NozMsg[2],NozMsg[3]))
	    sendosc("/nozoid/name",''.join((NozMsg[2],NozMsg[3])))

         if ord(NozMsg[1]) >= 0xF3 and ord(NozMsg[1]) <= 0xF5:
            (val,) = struct.unpack_from('>H', NozMsg, 2)

            sendosc("/nozoid/osc",''.join((twoDigit(ord(NozMsg[1])-0x9F),str(val-32767))))

         if ord(NozMsg[1]) >= 0xF6 and ord(NozMsg[1]) <= 0xF8:
	    #NozMsgL=NozMsg+Mser.read(2)
            (val,) = struct.unpack_from('>h', NozMsg, 2)
            sendosc("/nozoid/osc",''.join((twoDigit(ord(NozMsg[1])-0x9F),str(val))))
            #sendosc("/nozoid/mix",''.join((twoDigit(ord(NozMsg[1])-0xF5),str(val))))


'''
except StopIteration:
    print ("No Nozoid or DMX device found")
    print Mser
    Mser = False
    
if Mser != False:
    pass
'''
