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

import sys
from serial.tools import list_ports
import serial,time
from threading import Thread
import gstt,socket
import struct
from OSC import OSCServer, OSCClient, OSCMessage
import types

oscIPin = "10.255.255.194"
oscIPin = "127.0.0.1"
oscIPin = socket.gethostbyname(socket.gethostname())
oscPORTin = 8003
oscpathin = ""

oscIPout = "10.255.255.194"
#oscIPout = socket.gethostbyname(socket.gethostname())
oscPORTout = 8001

oscdevice = 0

NozMsg=[0,0,0,0]

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

    oscmsg = OSCMessage()
    oscmsg.setAddress(oscaddress)
    oscmsg.append(oscargs)
    
    print "sendosc: ", oscIPout,":",oscPORTout," ",oscmsg," args: ", oscargs
    try:
        osclient.sendto(oscmsg, (oscIPout, oscPORTout))
        oscmsg.clearData()
    except:
        print ('Connection refused at ',oscIPout)
        pass
    #time.sleep(0.001)



# sendme(oscaddress, [arg1, arg2,...])
osclientme.connect((oscIPin, oscPORTin)) 

def sendme(oscaddress,oscargs):
#def sendme(oscargs):
        
    oscmsg = OSCMessage()
    oscmsg.setAddress(oscaddress)
    oscmsg.append(oscargs)
    
    print "sending me : ", oscIPin,":",oscPORTin," ",oscmsg," args: ", oscargs
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


    
#
# OSC messages handlers
#
   
# default handler 
def handler(path, tags, args, source):

	
	oscpath = path.split("/")
	pathlength = len(oscpath)
	#print ""
	#print "default handler"
	#print "path:",path,"pathlength:", pathlength,"oscpath:", oscpath,"args:", args

	# /cc/number value
	if oscpath[1] == "cc" :
		number = int(oscpath[2])
		value = int(args[0])
		gstt.cc[number] = value    



# /on
def on(path, tags, args, source):
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
def stop(path, tags, args, source):

    print ("Stop Com from Nozoid")
    Mser.write([0xFF]) 
    time.sleep(1)
    print "In_Waiting garbage msg # after 0xFF sent:",Mser.in_waiting
    time.sleep(1)

    while Mser.in_waiting != 0:
        print "Still",Mser.in_waiting,"In_Waiting garbage msg after 0xFF sent"
	Mser.read()
    
# /name 
def name(path, tags, args, source):

    print ("asking for with nozoid type...")
    Mser.write([0xF0])
    time.sleep(1)
    print "In_Waiting garbage msg # after 0xF0 sent:",Mser.in_waiting
    time.sleep(1)
 
    
# /lfo
def lfo(path, tags, args, source):
	print "LFO"
	print "P:",path,",T:",tags,",A:",args,",S:",source
	print ("LFO ", args[0], "asked")
	Mser.write([0xA2 + int(args[0])]) # 0xA3 : LFO 1 / 0xA4 : LFO 2  / 0xA5 : LFO 3 


# /osc
def osc(path, tags, args, source):
	print "OSC"
	print ("OSC ", args[0], "asked")
	Mser.write([0x9F + int(args[0])]) # 0xA0 : OSC 1 / 0xA1 : OSC 2  / 0xA2 : OSC 3 

# /down
def down(path, tags, args, source):
	print ("DOWN ", args[0], "asked")
	Mser.write([0x9F + int(args[0])]) # 0xA0 : OSC 1 / 0xA1 : OSC 2  / 0xA2 : OSC 3 

# /up
def up(path, tags, args, source):
	print ("UP ", args[0], "asked")
	Mser.write([0x9F + int(args[0])]) # 0xA0 : OSC 1 / 0xA1 : OSC 2  / 0xA2 : OSC 3 

# /knob
def knob(path, tags, args, source):
	print ("KNOB", args[0], "asked")
	Mser.write([0 + int(args[0])]) # 0xA0 : OSC 1 / 0xA1 : OSC 2  / 0xA2 : OSC 3 


# Send text to status display widget
def status(text):
    sendosc("/status", text)

# registering all OSC message handlers

oscserver.addMsgHandler( "/on", on )
oscserver.addMsgHandler( "/stop", stop )
oscserver.addMsgHandler( "default", handler )
oscserver.addMsgHandler( "/name", name )
oscserver.addMsgHandler( "/lfo", lfo )
oscserver.addMsgHandler( "/osc", osc )
oscserver.addMsgHandler( "/up", up )
oscserver.addMsgHandler( "/down", down )
oscserver.addMsgHandler( "/knob", knob )


#
# Running...
#
    
        
# Search for nozoid

print("")
print("Available serial devices")
ports = list(list_ports.comports())
for p in ports:
    print(p)


try:

	# Find serial port
    #sernozoid = next(list_ports.grep("sbmodemFA131"))
    #sernozoid = next(list_ports.grep("sbmodem"))
    sernozoid = next(list_ports.grep("Due"))
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
    Mser.write([0xF0])
    #sendme("/lfo",1)
    sendme("/name","")
    
    while True:

        #print "loop"
        osc_frame()

	if Mser.in_waiting != 0:        
         NozMsg = Mser.read(4)

         if ord(NozMsg[1]) < 160:
            (val,) = struct.unpack_from('>H', NozMsg, 2)
            #print '/knob'.join(("/nozoid/knob/",str(ord(NozMsg[1]))," ",NozMsg[0:2].encode('hex'),":",str(val)))
            print ''.join(("/nozoid/knob/",str(ord(NozMsg[1]))," ",NozMsg[0:2].encode('hex')," ",str(val)))

            sendosc(''.join(("/nozoid/knob/",str(ord(NozMsg[1])))),str(val))
        
         if ord(NozMsg[1]) > 160:
        
            (val,) = struct.unpack_from('>h', NozMsg, 2)
            #print type(NozMsg[0:2].encode('hex'))
            #print type(ord(val))
            #print ''.join(("/nozoid/oscitruc/",str(ord(NozMsg[1])-0x9F)," ",NozMsg[0:2].encode('hex')," ",str(val)))
            #sendosc(''.join(("/nozoid/oscitruc/",str(ord(NozMsg[1])-0x9F)," ",NozMsg[0:2].encode('hex'),":",str(val))),"")
            
            sendosc("/nozoid/osc/0",val)
            sendosc("/nozoid/osc/1",val)
            sendosc("/nozoid/osc/2",val)   
                     
         if ord(NozMsg[1]) == 0xF0:   
            print ''.join((NozMsg[2],NozMsg[3]))


except StopIteration:
    print ("No Nozoid device found")
    Mser = False
    
if Mser != False:
    pass
 






