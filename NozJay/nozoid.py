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
import gstt
import struct

cc = [0] * 256

NozMsg=[0,0,0,0]

def twoDigitHex( number ):
   return '%02x' % number
   
def send(channel):
    Mser.write([channel]) 
    
def XXXNozMsg(channel,value):
    
    print channel
    print value
    
    
# Process events coming from Mcontroller (midi over serial version) in a separate thread. 
def MSerialinProcess():

    MESSAGE = 0xFF
    
    sermsg = [0,0,0,0,0,0]
    
    # pack bytes from serial port by 4. 
    
    while True:
        sermsg[0] = ord(Mser.read())
        if sermsg[0] == MESSAGE:

            sermsg[1]= ord(Mser.read()[0])
            sermsg[2]= twoDigitHex(ord(Mser.read()[0]))
            sermsg[3]= twoDigitHex(ord(Mser.read()[0]))
            sermsg[4]= twoDigitHex(ord(Mser.read()[0]))
            sermsg[5]= twoDigitHex(ord(Mser.read()[0]))
            
            valhxx = "".join((str(sermsg[2]),str(sermsg[3]),str(sermsg[4]),str(sermsg[5])))
            XXXNozMsg(sermsg[1],valhxx)
            
        time.sleep(0.02)
        
        
# Search for nozoid

print("")
print("Available serial devices")
ports = list(list_ports.comports())
for p in ports:
    print(p)

#raw_input("Will try to select Last Serial Port\nPress Enter to continue...")

try:
    sernozoid = next(list_ports.grep("ACM1"))
    #sernozoid = max(enumerate(list_ports.grep("tty*")))[1] #return the last serial port (see https://stackoverflow.com/questions/2138873/cleanest-way-to-get-last-item-from-python-iterator)
    print "Serial Picked for Nozoid :",sernozoid[0]
    Mser = serial.Serial(sernozoid[0],115200)
    #Mser = serial.Serial(gstt.sernozoid[0],115200,timeout=5)
    print "Serial connection..."
    print "Device..." 
    
#    Mser.open()
    print(Mser.is_open)
#    raw_input("Press Enter to continue...")

    print "In_Waiting garbage msg # at the serial opening:",Mser.in_waiting
    #print "Out_Waiting garbage msg # at the serial opening:",Mser.out_waiting
    #while Mser.out_waiting != 0 or Mser.in_waiting != 0:
    while Mser.in_waiting != 0:
        print "Still",Mser.in_waiting,"In_Waiting msg to flush at the opening"
	Mser.read()

    Mser.write([0xFF]) 
    time.sleep(1)
    print "In_Waiting garbage msg # after 0xFF sent:",Mser.in_waiting
    time.sleep(1)

    #while Mser.out_waiting != 0 or Mser.in_waiting != 0:
    while Mser.in_waiting != 0:
        print "Still",Mser.in_waiting,"In_Waiting garbage msg after 0xFF sent"
	Mser.read()

#    raw_input("Press Enter to continue...")

    Mser.write([0xF0])
    time.sleep(1)
    print "In_Waiting garbage msg # after 0xF0 sent:",Mser.in_waiting
    time.sleep(1)

#    while Mser.out_waiting != 0 or Mser.in_waiting != 0:
#        print "Still",Mser.in_waiting,"In_Waiting garbage msg after 0xF0 sent"
#	Mser.read()

    for i in range(2):
	print "!!"
        #print twoDigitHex(ord(Mser.read()[0])), twoDigitHex(ord(Mser.read()[0])), twoDigitHex(ord(Mser.read()[0])), twoDigitHex(ord(Mser.read()[0])), twoDigitHex(ord(Mser.read()[0])), twoDigitHex(ord(Mser.read()[0]))
        print twoDigitHex(ord(Mser.read()[0])), twoDigitHex(ord(Mser.read()[0])), twoDigitHex(ord(Mser.read()[0])), twoDigitHex(ord(Mser.read()[0]))


    print "In_Waiting garbage msg # after cleaning up try:",Mser.in_waiting

    time.sleep(1)
    #raw_input("Press Enter to continue...")

#    Mser.write([0x01])
#    for i in range(2):
#        print twoDigitHex(ord(Mser.read()[0])), twoDigitHex(ord(Mser.read()[0])), twoDigitHex(ord(Mser.read()[0])), twoDigitHex(ord(Mser.read()[0])), twoDigitHex(ord(Mser.read()[0])), twoDigitHex(ord(Mser.read()[0]))
    
#    Mser.write([0x02])
#    for i in range(2):
#        print twoDigitHex(ord(Mser.read()[0])), twoDigitHex(ord(Mser.read()[0])), twoDigitHex(ord(Mser.read()[0])), twoDigitHex(ord(Mser.read()[0])), twoDigitHex(ord(Mser.read()[0])), twoDigitHex(ord(Mser.read()[0]))
    
#    Mser.write([0x03])
#    for i in range(2):
#        print twoDigitHex(ord(Mser.read()[0])), twoDigitHex(ord(Mser.read()[0])), twoDigitHex(ord(Mser.read()[0])), twoDigitHex(ord(Mser.read()[0])), twoDigitHex(ord(Mser.read()[0])), twoDigitHex(ord(Mser.read()[0]))
    
#    raw_input("Press Enter to continue...")


    #Mser.write([0xA0]) #mod_osc1
    #Mser.write([0xA1]) #mod_osc2
    #Mser.write([0xA2]) #mod_osc3

    #Mser.write([0xA3]) #mod_lfo1
    #Mser.write([0xA4]) #mod_lfo2
    #Mser.write([0xA5]) #mod_lfo3

    while True:
        #print twoDigitHex(ord(Mser.read()[0])), twoDigitHex(ord(Mser.read()[0])), twoDigitHex(ord(Mser.read()[0])), twoDigitHex(ord(Mser.read()[0])), twoDigitHex(ord(Mser.read()[0])), twoDigitHex(ord(Mser.read()[0]))
	#int(Mser.read()[0],16)    
	#print(ord(Mser.read(2)[0]))
	
	#NozMsg[0]=Mser.read()
	#NozMsg[1]=Mser.read()
	#NozMsg[2]=Mser.read()
	#NozMsg[3]=Mser.read()
	NozMsg = Mser.read(4)
	#print NozMsg.encode('hex')

	#print type(NozMsg[0])
	#NozMsg[4]=Mser.read()
	#NozMsg[5]=Mser.read()

	#print struct.unpack(">H",NozMsg[0],NozMsg[1])

	#print struct.unpack(">H",Mser.read(2))[0],struct.unpack(">l",Mser.read(4))[0]
	#print struct.unpack(">H",Mser.read(2))[0],struct.unpack(">h",Mser.read(2))[0]

        #print twoDigitHex(ord(NozMsg[0])), twoDigitHex(ord(NozMsg[1]))

	#print struct.unpack(struct.unpack(">H",NozMsg[2:4]))[0]

	#print "".join(NozMsg[2:4])
	#print twoDigitHex(ord(NozMsg[1]))
	#if NozMsg[1] < 160:

#	if ord(NozMsg[1]) < 160:
#		#print "NozMsg < 160"
#		#print NozMsg[1]
#	        #print twoDigitHex(ord(NozMsg[0])), twoDigitHex(ord(NozMsg[1])), struct.unpack(">H","".join(NozMsg[2:4]))[0]
#		(val,) = struct.unpack_from('>H', NozMsg, 2)
#		print NozMsg[0:2].encode('hex'), val
#	else:
#		#print "NozMsg > 160"
#		#print NozMsg[1]
#        	#print twoDigitHex(ord(NozMsg[0])), twoDigitHex(ord(NozMsg[1])), struct.unpack(">h","".join(NozMsg[2:4]))[0]
#		(val,) = struct.unpack_from('>h', NozMsg, 2)
#		print NozMsg[0:2].encode('hex'), val

        if ord(NozMsg[1]) < 160:
            (val,) = struct.unpack_from('>H', NozMsg, 2)
            #print '/nozoid//knob'.join((str(ord(NozMsg[1]))," ",NozMsg[0:2].encode('hex'),":",str(val)))
            print ''.join((str(ord(NozMsg[1]))," ",NozMsg[0:2].encode('hex'),":",str(val)))
            #sendosc("/nozoid/knob",''.join((str(ord(NozMsg[1])),NozMsg[0:2].encode('hex'),":",str(val))))
            #sendosc("/nozoid/knob",''.join((str(ord(NozMsg[1])),str(val))))

        if ord(NozMsg[1]) >= 0xA0 and ord(NozMsg[1]) < 0xF0:
            (val,) = struct.unpack_from('>h', NozMsg, 2)
            #print type(NozMsg[0:2].encode('hex'))
            #print type(ord(val))
            #print '/nozoid/oscitruc'.join((str(ord(NozMsg[1])-0x9F)," ",NozMsg[0:2].encode('hex'),":",str(val)))
            print ''.join((str(ord(NozMsg[1])-0x9F)," ",NozMsg[0:2].encode('hex'),":",str(val)))
            #sendosc("/nozoid/osc",''.join((str(ord(NozMsg[1])-0x9F),str(val))))

        if ord(NozMsg[1]) == 0xF0:
                print ''.join((NozMsg[2],NozMsg[3]))
                #sendosc("/nozoid/name",''.join((NozMsg[2],NozMsg[3])))

        if ord(NozMsg[1]) >= 0xF3 and ord(NozMsg[1]) <= 0xF5:
	    #NozMsg=NozMsg.join((Mser.read(2)))
	    #NozMsg=NozMsg+Mser.read(2)
            (val,) = struct.unpack_from('>H', NozMsg, 2)
            print ''.join((str(ord(NozMsg[1])-0x9F)," ",NozMsg[0:2].encode('hex')," ",NozMsg[2:4].encode('hex'),":",str(val)))

        if ord(NozMsg[1]) >= 0xF6 and ord(NozMsg[1]) <= 0xF8:
	    #NozMsg=NozMsg.join((Mser.read(2)))
	    #NozMsg=NozMsg+Mser.read(2)
            (val,) = struct.unpack_from('>h', NozMsg, 2)
            print ''.join((str(ord(NozMsg[1])-0x9F)," ",NozMsg[0:2].encode('hex')," ",NozMsg[2:4].encode('hex'),":",str(val)))

	#print NozMsg[2:4]


	#print struct.unpack("<B",Mser.read(1))[0],struct.unpack("<B",Mser.read(1))[0],struct.unpack("<l",Mser.read(4))[0]
	



    #Mser.write(bytes([int(113)]))
    #thread = Thread(target=MSerialinProcess, args=())
    #thread.setDaemon(True)
    #thread.start()
    
except StopIteration:
    print ("No Nozoid device found")
    Mser = False
    
if Mser != False:
    pass
 
    #MSerialinProcess()

# Search for enttec usb pro

try:
    
    gstt.serdmx = next(list_ports.grep("/dev/ttyACM1"))
    print "Serial Picked for DMX : ", gstt.serdmx[0]
    
    #serDMX = serial.Serial(gstt.serdmx[0],9600) 
    #Mser.write(bytes([int(113)]))
    #thread = Thread(target=MSerialinProcess, args=())
    #thread.setDaemon(True)
    #thread.start()
    
except StopIteration:
    print ("No DMX device found")

print ""
