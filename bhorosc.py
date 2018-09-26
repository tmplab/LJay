# coding=UTF-8
"""

OSC Manager 

by Sam Neurohack 
from /team/laser

"""
#chercher dans doc pyosc multiclient pour subscribe...
# pydoc OSC


from OSC import OSCServer, OSCClient, OSCMessage
import types, time

import bhoreal
import launchpad
import orbits
from globalVars import *
import gstt
import midi
import socket
import colorify


import mydmx
#import oscled
#import oscdefault
#import runmode

oscIPin = socket.gethostbyname("")
#oscIPin = "192.168.1.10"
#oscPORTin = 8001
oscPORTin = gstt.iport
oscpathin = ""

oscIPout = ""
#oscPORTout = 8002
oscPORTout = gstt.oport

oscIPresol = "127.0.0.1"
oscPORTresol = 7000
	
oscdevice = 0

padrightsnotes = [0,120,104,88,72,56,40,24,56]

controlmatrix = ["","Laser","Synth","Leds","DMX","Midi"]
print (controlmatrix[1])
CurrentMidiDevice =0

lasermatrix = [["Select","Align","Prog","Curve",""],["ON","OFF","","",""],["Number","<",">","",""],["Pong","","","",""],["Kepler","Lissa","","","Select"],["","","","",""]]

synthmatrix = [["Select","OSC","LFO","",""],["Freq","","","",""],["","","","",""],["","","","",""],["","","","",""],["","","","",""]]
ledsmatrix = [["Bhoreal","Lpad","","",""],["CLS","","","",""],["CLS","","","",""],["","","","",""],["","","","",""],["","","","",""]]
dmxmatrix = [["Select","Chan","Val","DMX","DMX"],["","","","",""],["","","","",""],["","","","",""],["","","","",""],["","","","",""]]
midimatrix =  [["List","Check","Serial","Nozoid",""],["<",">","","",""],["","","","",""],["","","","",""],["","","","",""],["","","","",""]]
currentmatrix = 1
matrix = lasermatrix
line2 = 1
line3 = 1



print("")
print("Starting OSCServer...")
print ("Receiving on ", oscIPin, ":",str(oscPORTin))
oscserver = OSCServer( (oscIPin, oscPORTin) )
oscserver.timeout = 0
OSCRunning = True


def handle_timeout(self):
    self.timed_out = True

oscserver.handle_timeout = types.MethodType(handle_timeout, oscserver)


osclient = OSCClient()
osclientme = OSCClient()

# 
osclient3 = OSCClient()
osclient4 = OSCClient()
osclient5 = OSCClient()
osclient6 = OSCClient()

osclientresol = OSCClient()

oscmsg = OSCMessage()


# sendosc(oscaddress, [arg1, arg2,...])
def sendosc(oscaddress,oscargs):
    
    # also works : osclient.send(OSCMessage("/led", oscargs))

    oscmsg = OSCMessage()
    oscmsg.setAddress(oscaddress)
    oscmsg.append(oscargs)
    
    print "sending : ",oscmsg
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
        
    oscmsg = OSCMessage()
    oscmsg.setAddress(oscaddress)
    oscmsg.append(oscargs)
    
    print "sending me: ",oscmsg
    try:
        osclientme.sendto(oscmsg, (oscIPin, oscPORTin))
        oscmsg.clearData()
    except:
        print ('Connection to myself refused')
        pass
    #time.sleep(0.001)
   
# send3(oscaddress, [arg1, arg2,...])
osclient3.connect((oscIPin, 8003)) 
def send3(oscaddress,oscargs):
        
    oscmsg = OSCMessage()
    oscmsg.setAddress(oscaddress)
    oscmsg.append(oscargs)
    
    #print "sending to 3 : ",oscmsg
    try:
        osclient3.sendto(oscmsg, (oscIPin, 8003))
        oscmsg.clearData()
    except:
        print ('Connection to 3 refused')
        pass
    #time.sleep(0.001)
    
# send4(oscaddress, [arg1, arg2,...])
osclient4.connect((oscIPin, 8004)) 
def send4(oscaddress,oscargs):
        
    oscmsg = OSCMessage()
    oscmsg.setAddress(oscaddress)
    oscmsg.append(oscargs)
    
    print "sending to 4 : ",oscmsg
    try:
        osclient4.sendto(oscmsg, (oscIPin, 8004))
        oscmsg.clearData()
    except:
        print ('Connection to 4 refused')
        pass
    #time.sleep(0.001)
    
    
# send5(oscaddress, [arg1, arg2,...])
osclient5.connect((oscIPin, 8005)) 
def send5(oscaddress,oscargs):
        
    oscmsg = OSCMessage()
    oscmsg.setAddress(oscaddress)
    oscmsg.append(oscargs)
    
    print "sending to 5 : ",oscmsg
    try:
        osclient5.sendto(oscmsg, (oscIPin, 8005))
        oscmsg.clearData()
    except:
        print ('Connection to 5 refused')
        pass
    #time.sleep(0.001)
    

# send6(oscaddress, [arg1, arg2,...])
osclient6.connect((oscIPin, 8006)) 
def send6(oscaddress,oscargs):
        
    oscmsg = OSCMessage()
    oscmsg.setAddress(oscaddress)
    oscmsg.append(oscargs)
    
    print "sending to 6 : ",oscmsg
    try:
        osclient6.sendto(oscmsg, (oscIPin, 8006))
        oscmsg.clearData()
    except:
        print ('Connection to 6 refused')
        pass
    #time.sleep(0.001)

# Send to Resolume
# sendresol(oscaddress, [arg1, arg2,...])
# sendresol("/noteon",note)
osclientresol.connect((oscIPresol, oscPORTresol)) 
def sendresol(oscaddress,oscargs):
        
    oscmsg = OSCMessage()
    oscmsg.setAddress(oscaddress)
    oscmsg.append(oscargs)
    
    print "sending to Resolume : ",oscmsg
    try:
        osclientresol.sendto(oscmsg, (oscIPresol, oscPORTresol))
        oscmsg.clearData()
    except:
        print ('Connection to Resolume refused')
        pass
    #time.sleep(0.001)

jumplaser =  {
        3: send3,
        4: send4,
        5: send5,
        6: send6
    }       

#
# Main paths
#

# /quit
def quit(path, tags, args, source):

    print "Quit OSC"


# /runmode number 
# "Prompt"   = 10
# "Myxo"     = 2
# "Midifile" = 3
def padmode(path, tags, args, source):
    user = ''.join(path.split("/"))
    print "/padmode : ",user,args
    padmode.PadMode(args[0])


# /on
def on(path, tags, args, source):
    global oscIPout,oscdevice,controlmatrix

    user = ''.join(path.split("/"))
    #print "New OSC Client : " + str(source[0])
    oscIPout = str(source[0])
    osclient.connect((oscIPout, oscPORTout))
    #print ("Sending on ", oscIPout, ":",str(oscPORTout))
    print ""
    print osclient
    oscdevice = 1
    sendosc("/on", 1)
    sendosc("/off", 0)
    sendosc("/cc/5", 60)
    sendosc("/cc/6", 60)
    sendosc("/rot/x", 0)
    sendosc("/rot/y", 0)
    sendosc("/rot/z", 0)
        
    status("MController ON")
    currentmatrix = 1
    matrixledsoff()
    displaymatrix(1)


# /off
def off(path, tags, args, source):
    global oscdevice

    user = ''.join(path.split("/"))
    sendosc("/off", 1)
    sendosc("/on", 0)
    status("MController OFF")
    oscdevice = 0



# Send text to status display widget if one is connected
def status(text):
	if oscdevice == 1:
		sendosc("/status", text)
	else:
		print text



# RAW OSC Frame available ? 
def osc_frame():
    # clear timed_out flag
    oscserver.timed_out = False
    # handle all pending requests then return
    while not oscserver.timed_out:
        oscserver.handle_request()



# /noteon number velocity
def noteon(path, tags, args, source):
    user = ''.join(path.split("/"))
    print ""
    print path,args
    #print "note : ", args[0]
    #print "velocity : 127"
    
    if gstt.tomidi and args[0] > 11:
    	print "Sending to midi devices"
        midi.NoteOn(int(args[0]),64)

    else:
    	noteupdate(int(args[0]))


# /noteoff number 
def noteoff(path, tags, args, source):
    user = ''.join(path.split("/"))
    print ""
    print user,path,args
    print "note : ", args[0]
    print "velocity : ", 0
    midi.NoteOff(int(args[0]))
    status(''.join(("note off ", str(args[0]))))
 
# Update Laser 
def noteupdate(note):

	'''
	# forward new instruction ? 
	if gstt.MyLaser != gstt.Laser:
		doit = jumplaser.get(gstt.Laser)
		doit("/noteon",note)
	'''
	# change Curve
	if note < 8:
		gstt.Curve = note
		status(''.join(("New Curve : ",str(gstt.Curve))))
		bhoreal.UpdateLine(1,gstt.Curve+1)
	
	# change Set. Use black curve waiting for new Curve
	if note > 7 and note < 16:
		gstt.Curve = -1
		gstt.Set = note - 8
		status(''.join(("New Set : ",str(gstt.Set))))
		bhoreal.UpdateLine(2,gstt.Set +1)

	# change current laser
	if  note > 15 and note < 24:
		gstt.Laser = note -13
		status(''.join(("New Laser : ",str(gstt.Laser))))
		bhoreal.UpdateLine(3, gstt.Laser +1)

	# change current simulator PL
	if  note > 23 and note < 32:
		gstt.simuPL = note - 24
		status(''.join(("New Simu PL : ",str(gstt.SimuPL))))
		bhoreal.UpdateLine(4, gstt.simuPL +1)

	if note == 57 or note == 58:
		gstt.colormode = note- 56
		status(''.join(("New Color Mode : ",str(gstt.colormode))))

	if note > 58:
		status(''.join((str(args[0])," on Laser ",str(gstt.Laser))))

# Update Laser cc
def ccupdate(cc,value):

 	gstt.cc[cc]=value

# /gyrosc/gyro x y z 
def gyro(path, tags, args, source):
    user = ''.join(path.split("/"))
    print ""
    print user,path,args
    
    gstt.cc[29]=args[0]*60
    
    # Y rotation cc 30
    gstt.cc[30]=args[1]*60
    
    # X rotation cc 29
    gstt.cc[31]=0
    #gstt.cc[31]=args[2]*127
    
    print gstt.cc[29],gstt.cc[30],gstt.cc[31]
 
 
# /accxyz x y z 
def accxyztouchosc(path, tags, args, source):
    user = ''.join(path.split("/"))
    
    #print ""
    #print user,path,args
    
    gstt.cc[2] += int(args[0]* 10)
    #print "deltax", int(args[0]*5)
    # Y rotation cc 30
    gstt.cc[1] += int(args[1]*10)
    
    # X rotation cc 29
    #gstt.cc[5] += int(args[2]*30)
    #gstt.cc[31]=args[2]*127
    
    #print gstt.cc[29],gstt.cc[30],gstt.cc[31]


# /point x y z 
def point(path, tags, args, source):
    user = ''.join(path.split("/"))
    #print ""
    #print user,path,args
    
    # X
    gstt.point[0]=args[0]
    
    # Y
    gstt.point[1]=args[1]
    
    # Color
    gstt.point[2]= args[2]
    
    #print gstt.point[0],gstt.point[1],gstt.point[2]

# 
# Nozosc commands for Nozoids synthetizer
#
# /nozoid/offset value = decalage X, decalage Y, courbe
def nozoffset(path, tags, args, source):
    user = ''.join(path.split("/"))
    print "Here we are in /nozoid/offset in bhorosc"
    gstt.curveNumber = int(args[2])
    gstt.offsetX[gstt.curveNumber] = int(args[0])
    gstt.offsetY[gstt.curveNumber] = int(args[1])
    print "offsetX=%d,offsetY=%d,curveNumber=%d"%(gstt.offsetX[gstt.curveNumber],gstt.offsetY[gstt.curveNumber],gstt.curveNumber)

# /nozoid/X value = numéro d'oscillateur
def nozX(path, tags, args, source):
    user = ''.join(path.split("/"))
    print "Here nozX in bhorosc"
    #print user,path,args
    print path,args
    oscillator = int(args[0])
    curveNumber = int(args[1])
    print "Oscillator=%d,CurveNumber=%d"%(oscillator,curveNumber)
    print "Setting gstt.X[%d] to %d" %(curveNumber,oscillator)
    gstt.X[curveNumber] = oscillator

    if oscillator == 0:
	gstt.colorX[curveNumber][0]=0
	gstt.colorX[curveNumber][1]=0
	gstt.colorX[curveNumber][2]=0
    if oscillator == 1:
	gstt.colorX[curveNumber][0]=255
	gstt.colorX[curveNumber][1]=0
	gstt.colorX[curveNumber][2]=0
    if oscillator == 2:
	gstt.colorX[curveNumber][0]=0
	gstt.colorX[curveNumber][1]=255
	gstt.colorX[curveNumber][2]=0
    if oscillator == 3:
	gstt.colorX[curveNumber][0]=255
	gstt.colorX[curveNumber][1]=255
	gstt.colorX[curveNumber][2]=0
    if oscillator == 4:
	gstt.colorX[curveNumber][0]=0
	gstt.colorX[curveNumber][1]=0
	gstt.colorX[curveNumber][2]=255
    if oscillator == 5:
	gstt.colorX[curveNumber][0]=255
	gstt.colorX[curveNumber][1]=0
	gstt.colorX[curveNumber][2]=255
    if oscillator == 6:
	gstt.colorX[curveNumber][0]=0
	gstt.colorX[curveNumber][1]=255
	gstt.colorX[curveNumber][2]=255
    if oscillator >= 7:
	gstt.colorX[curveNumber][0]=255
	gstt.colorX[curveNumber][1]=255
	gstt.colorX[curveNumber][2]=255

    colorify.XY(curveNumber)

    #gstt.OscXY[1] = gstt.X
	
# Get wich Nozoid sound curve to draw on Y axis 
def nozY(path, tags, args, source):
    user = ''.join(path.split("/"))
    print "Here nozY in bhorosc"
    #print user,path,args
    print path,args
    oscillator = int(args[0])
    curveNumber = int(args[1])
    print "Oscillator=%d,CurveNumber=%d"%(oscillator,curveNumber)
    print "Setting gstt.Y[%d] to %d" %(curveNumber,oscillator)
    gstt.Y[curveNumber] = oscillator

    if oscillator == 0:
	gstt.colorY[curveNumber][0]=0
	gstt.colorY[curveNumber][1]=0
	gstt.colorY[curveNumber][2]=0
    if oscillator == 1:
	gstt.colorY[curveNumber][0]=255
	gstt.colorY[curveNumber][1]=0
	gstt.colorY[curveNumber][2]=0
    if oscillator == 2:
	gstt.colorY[curveNumber][0]=0
	gstt.colorY[curveNumber][1]=255
	gstt.colorY[curveNumber][2]=0
    if oscillator == 3:
	gstt.colorY[curveNumber][0]=255
	gstt.colorY[curveNumber][1]=255
	gstt.colorY[curveNumber][2]=0
    if oscillator == 4:
	gstt.colorY[curveNumber][0]=0
	gstt.colorY[curveNumber][1]=0
	gstt.colorY[curveNumber][2]=255
    if oscillator == 5:
	gstt.colorY[curveNumber][0]=255
	gstt.colorY[curveNumber][1]=0
	gstt.colorY[curveNumber][2]=255
    if oscillator == 6:
	gstt.colorY[curveNumber][0]=0
	gstt.colorY[curveNumber][1]=255
	gstt.colorY[curveNumber][2]=255
    if oscillator >= 7:
	gstt.colorY[curveNumber][0]=255
	gstt.colorY[curveNumber][1]=255
	gstt.colorY[curveNumber][2]=255

    colorify.XY(curveNumber)
    #gstt.OscXY[2] = gstt.Y

def nozcolor(path, tags, args, source):
	#print "here we are in nozcolor!"
	#print "args",args
	if len(args) <= 1:
	  if len(args) == 0:
	    curveNumber = 0
	  if len(args) == 1:
	    curveNumber = int(args[0])
	  print "Here is Curve[%d]'s color R:%d G:%d B:%d" % (curveNumber,gstt.curveColor[curveNumber][0],gstt.curveColor[curveNumber][1],gstt.curveColor[curveNumber][2])

	else:
	  if len(args) > 3:
	    curveNumber = int(args[3])
	  else:
	    curveNumber = 0
	  print "Changing Curve[%d]'s color to R:%d G:%d B:%d" % (curveNumber,args[0], args[1], args[2])
	  gstt.curveColor[curveNumber][0]=int(args[0])
	  gstt.curveColor[curveNumber][1]=int(args[1])
	  gstt.curveColor[curveNumber][2]=int(args[2])

    
# default handler 
def handler(path, tags, args, source):

	
	oscpath = path.split("/")
	pathlength = len(oscpath)
	#print ""
	#print "default handler"
	#print path, oscpath, args


	# /control/matrix/Y/X 0 or 1
	if oscpath[1] == "control" and oscpath[2] == "matrix" and  args > 0:
		controlmatrixhandler(oscpath[4],oscpath[3],args)


	# /pad/yx/Y/X 0 or 1
	if oscpath[1] == "pad" and oscpath[2] == "yx":
		pass
		
		
		
	# /pad/rights/note 0 or 1	
	if oscpath[1] == "pad" and oscpath[2] == "rights":
		
		# noteon
		if args[0] == 1:		
			note = padrightsnotes[int(oscpath[3])]
			#print "noteon : ", str(note) 
			sendme("/noteon",note)
		
		# noteoff
		if args[0] == 0:		
			note = padrightsnotes[int(oscpath[3])]
			#print "noteoff : ", str(note) 
			sendme("/noteoff",note)
		
		
	# /pad/tops/cc 0 or 1	
	if oscpath[1] == "pad" and oscpath[2] == "tops":
		
		# cc 127
		if args[0] == 1:		
			print "cc : ", str(int(oscpath[4])+103)
			sendme(''.join(["/cc/",str(int(oscpath[4])+103)]), 127)
			status(''.join((oscpath[4]," to 127")))
			 
		# cc 0
		if args[0] == 0:		
			print "cc : ", str(int(oscpath[4])+103)
			sendme(''.join(["/cc/",str(int(oscpath[4])+103)]), 0)
			status(''.join((oscpath[4]," to 0")))


	'''
	Forward/send cc to some other osc server
	# Not my laser -> forward to slave
	if oscpath[1] == "cc" and gstt.MyLaser != gstt.Laser:
		value = int(args[0])
		doit = jumplaser.get(gstt.Laser)
		doit(path,value)
	'''

	# Midi from LPD8 via midiosc

	#if oscpath[1] == "midi" and oscpath[2] == "LPD8":


	# /cc/number value
	if oscpath[1] == "cc":
		number = int(oscpath[2])
		value = int(args[0])
		gstt.cc[number] = value
		
		print number 
		print value
		
		#print "29: ", str(gstt.cc[29])," 30: ", str(gstt.cc[30])," 31: ", str(gstt.cc[31])
		
		# send cc to midi devices
		if gstt.tomidi == True:
			midi.MidiMsg((midi.CONTROLLER_CHANGE,number,value))
			status(''.join((oscpath[2]," to ", str(value))))


		# send cc to dmx channel
		if gstt.todmx == True:
			if gstt.serdmx != "":
				mydmx.send(number,value*2)
				status(''.join((oscpath[2]," to ", str(value*2))))
			else:
				status("DMX error")

		# Use cc to align laser
		if gstt.tolaser == True and line2 == "Align":
			if number == 1:
				gstt.centerX[gstt.Laser]  = value * 20	
			if number == 2:
				gstt.centerY[gstt.Laser]  = value * 20
				
		# Use cc to change curve parameters
		if gstt.tolaser == True and line2 == "Curve":
			if number == 1:
				gstt.centerX[gstt.Laser]  = value * 20				



	# /number
	if oscpath[1] < "9" and oscpath[1] > "0" and len(oscpath[1])==1 and args[0] > 0:

		if gstt.tolaser == True and line2 == "Curve" and line3 == "Select":
			status(oscpath[1])
			gstt.mode = oscpath[1]

		else: 	
			gstt.newnumber += oscpath[1]
			print gstt.newnumber
			status(gstt.newnumber)

		
	# /clear
	if  oscpath[1] == "clear"  and args[0] > 0:
		gstt.newnumber = ""
		status(gstt.newnumber)

		
	# /enter
	if  oscpath[1] == "enter"  and args[0] > 0:
	
		# new laser number
		if gstt.tolaser == True and line2 == "Select":
			print gstt.newnumber, args
			status(''.join(("Laser : ",gstt.newnumber)))
			gstt.currentlaser = int(gstt.newnumber)
		gstt.newnumber = ""
		
	# /red
	if  oscpath[1] == "red"  and args[0] > 0:
		gstt.color[0] = 255
		status("Red On")		

	if  oscpath[1] == "red"  and args[0] == 0:
		gstt.color[0] = 0
		status("Red Off")		

	#print gstt.color		


	# /green
	if  oscpath[1] == "green"  and args[0] > 0:
		gstt.color[1] = 255
		status("Green On")

	if  oscpath[1] == "green"  and args[0] == 0:
		gstt.color[1] = 0
		status("Green Off")	

	#print gstt.color		


	# /blue
	if  oscpath[1] == "blue"  and args[0] > 0:
		gstt.color[2] = 255
		status("Blue On")		

	if  oscpath[1] == "blue"  and args[0] == 0:
		gstt.color[2] = 0
		status("Blue Off")	
	#print gstt.color		

	# 
	# Nozoids
	# 
	
	# /nozoid/mix/number value	
	if oscpath[1] == "nozoid" and oscpath[2] == "mix":
		number = int(oscpath[3])
		value = int(args[0])
		print "mix",number,value
		#gstt.OscXY[0] = gstt.mix
		gstt.mix[number] = value
	
	# /nozoid/vco/number value	
	if oscpath[1] == "nozoid" and oscpath[2] == "vco":
		number = int(oscpath[3])
		value = int(args[0])
		print "vco",number,value
		#gstt.OscXY[0] = gstt.vco
		gstt.vco[number] = value
	
	# /nozoid/lfo/number value	
	if oscpath[1] == "nozoid" and oscpath[2] == "lfo":
		number = int(oscpath[3])
		value = int(args[0])
		print "lfo",number,value
		#gstt.OscXY[0] = gstt.lfo
		gstt.lfo[number] = value
	
	# /nozoid/osc/number value	
	if oscpath[1] == "nozoid" and oscpath[2] == "osc":
		number = int(oscpath[3])#the oscillator/modulator number asked
		value = int(args[0])#the value of the oscillation/modulation
		#print "osc",number,value
		#gstt.OscXY[0] = gstt.osc
		#this is where we save the value of the current oscillation value of the osc/lfo/cv etc (aka number)
		gstt.osc[number] = value
	
	# /nozoid/knob/number value	
	if oscpath[1] == "nozoid" and oscpath[2] == "knob":
		number = int(oscpath[3])
		value = int(args[0])
		print "knob",number,value
		gstt.knob[number] = value
	
	
			
# Control matrix handler
def controlmatrixhandler(x,y,args):
	global currentmatrix,matrix,controlmatrix
	global line2,line3,CurrentMidiDevice
	
	print "button = " ,x,y,args
	
	# First raw of control matrix
	if y == '1':
		currentmatrix = int(x)
		
		gstt.tolaser = gstt.tosynth = gstt.toleds = gstt.todmx = gstt.tomidi = False
		# Switch to laser
		if currentmatrix == 1:
			matrix = lasermatrix
			gstt.tolaser = True
			if gstt.debug == 1:
				print "To Laser On"
				
		# Switch to Synth		
		if currentmatrix == 2:
			matrix = synthmatrix
			gstt.tosynth = True		
			if gstt.debug == 1:
				print "To Synth On"
				
		# Switch to leds	
		if currentmatrix == 3:
			matrix = ledsmatrix	
			gstt.toleds = True	
			if gstt.debug == 1:
				print "To Leds On"
				
		# Switch to DMX
		if currentmatrix == 4:
			matrix = dmxmatrix
			gstt.todmx = True
			if gstt.debug == 1 and gstt.todmx == True:
				print "To DMX On"
				
		# Switch to Midi
		if currentmatrix == 5:
			gstt.tomidi = True
			matrix = midimatrix
			if gstt.debug == 1:
				print "To Midi On"
				
		matrixledsoff()
		sendosc(''.join(("/control/matrix/1/",str(currentmatrix),"/led")), 1)
		status(controlmatrix[currentmatrix])
		displaymatrix(x)

	if y == "2":
	
		# Second raw of control matrix : line2
		line2 = matrix[int(y)-2][int(x)-1]
		line3 = ""
		print controlmatrix[currentmatrix],line2,line3
		status(line2)
		for led in range(1,6):
			sendosc(''.join(("/control/matrix/2/",str(led),"/led")), 0)
			sendosc(''.join(("/control/matrix/3/",str(led),"/led")), 0)
		sendosc(''.join(("/control/matrix/2/",str(int(x)),"/led")), 1)
		displaymatrix(x)
		
		# List Midi Devices
		if gstt.tomidi == True and line2 == "List":
			status(''.join((str(midi.MidInsNumber)," devices")))
			CurrentMidiDevice = 0
		
		# Select laser
		if gstt.tolaser == True and line2 == "Select":
			status("Enter number")
		displaymatrix(x)

	
	if y == "3":

		# Second raw of control matrix : line3
		line3 = matrix[matrix[0].index(line2)+1][int(x)-1]
		print controlmatrix[currentmatrix],line2,line3
		
		#status(line3)
		for led in range(1,6):
			sendosc(''.join(("/control/matrix/3/",str(led),"/led")), 0)
		sendosc(''.join(("/control/matrix/3/",str(int(x)),"/led")), 1)
		#displaymatrix(x)
		
		
		# Display Midi Devices names
		if gstt.tomidi == True and line2 == "List" and line3 == ">"  and args[0] > 0:
			print CurrentMidiDevice
			print midi.midiname[CurrentMidiDevice]
			print "Session" in midi.midiname[CurrentMidiDevice]
			if "Session" in midi.midiname[CurrentMidiDevice]:
				status("Network Session")
			else:
				status(midi.midiname[CurrentMidiDevice])
			if CurrentMidiDevice < midi.MidInsNumber - 1:
				CurrentMidiDevice += 1

		if gstt.tomidi == True and line2 == "List" and line3 =="<":

			print CurrentMidiDevice
			print midi.midiname[CurrentMidiDevice]
			if "Session" in midi.midiname[CurrentMidiDevice]:
				status("Network Session")
			else:
				status(midi.midiname[CurrentMidiDevice])
			if CurrentMidiDevice > 0:
				CurrentMidiDevice -= 1

		if gstt.tolaser == True and line2 == "Align":
			gstt.mode = 0
			status("Use cc to align")


		# Curve change
		if line3 =="Lissa":
			gstt.Mode = 1
		if line3 =="Kepler":
			gstt.Mode = 2  			
					
# Display control matrix

def displaymatrix(x):
	global controlmatrix, matrix,currentmatrix
	
	print x
	print currentmatrix, matrix[int(x)]
	for button in range(1,6):
		sendosc(''.join(("/control/matrix/1/",str(button),"/text")), controlmatrix[button])
	for button in range(1,6):
		sendosc(''.join(("/control/matrix/2/",str(button),"/text")), matrix[0][button-1])
 	for button in range(1,6):
		sendosc(''.join(("/control/matrix/3/",str(button),"/text")), matrix[int(x)][button-1])


def matrixledsoff():

	for column in range(1,6):
		for raw in range(1,6):
			sendosc(''.join(("/control/matrix/",str(raw),"/",str(column),"/led")), 0)

#
# LEDS
#

# /led lednumber color
def led(path, tags, args, source):

    # tags will contain 'fff'
    # args is a OSCMessage with data
    # source is where the message came from (in case you need to reply)
    #print (source,path,args[0],args[1]) 
    
    user = ''.join(path.split("/"))
    midi.NoteOn(args[0],args[1])


# /led/xy x y color
def ledxy(path, tags, args, source):

    user = ''.join(path.split("/"))
    midi.NoteOnXY(args[0],args[1],args[2])


# /cls bhoreal
def clsbhor(path, tags, args, source):

    user = ''.join(path.split("/"))
    bhoreal.Cls()


# /allcolor bhoreal
def allcolorbhor(path, tags, args, source):

    user = ''.join(path.split("/"))
    bhoreal.AllColor(args[0])


# /xy x y
def xy(path, tags, args, source):

    user = ''.join(path.split("/"))
    midi.NoteOnXY(args[0],args[1],args[2])


# /pad/yx/Y/X (1 or 0) note from touchosc led matrix
def pad(path, tags, args, source):

	user = ''.join(path.split("/"))
	midi.NoteOnXY(args[0],args[1],args[2])


def stoprot(path, tags, args, source):
	gstt.cc[29]=0
	gstt.cc[30]=0
	gstt.cc[31]=0
	gstt.cc[22]=50

	gstt.angleX=0
	gstt.angleY=0
	gstt.angleZ=0
	


# Change simulator point list

# /display/PL/ pointlistnumber
def display(path, tags, args, source):
    user = ''.join(path.split("/"))
    print ""
    print user,path,args
    print "New Point list number for simulator : ", args[0]
    gstt.simuPL = args[0]
    
    status(''.join(("Simu point list : ", str(args[0]))))



#
# with AI OSC commands
#


# /ai/velocity 
def AiVelocity(path, tags, args, source):
    user = ''.join(path.split("/"))
    print ""
    print user,path,args
    print "Ai Velocity : ", args[0]
    gstt.aivelocity = args[0]
    
    status(''.join(("Ai Velocity : ", str(args[0])," on Laser ",str(gstt.Laser))))


# /ai/expressivity
def AiExpressivity(path, tags, args, source):
    user = ''.join(path.split("/"))
    print ""
    print user,path,args
    print "Ai Expressivity : ", args[0]
    gstt.aiexpressiviity = args[0]
    
    status(''.join(("Ai Expressivity : ", str(args[0])," on Laser ",str(gstt.Laser))))

# /ai/sensibility 
def AiSensibility(path, tags, args, source):
    user = ''.join(path.split("/"))
    print ""
    print user,path,args
    print "Ai Sensibility : ", args[0]
    gstt.aisensibility = args[0]
    
    status(''.join(("Ai Velocity : ", str(args[0])," on Laser ",str(gstt.Laser))))

# /ai/beauty
def AiBeauty(path, tags, args, source):
    user = ''.join(path.split("/"))
    print ""
    print user,path,args
    print "Ai Beauty : ", args[0]
    gstt.aibeauty = args[0]
    
    status(''.join(("Ai Beauty : ", str(args[0])," on Laser ",str(gstt.Laser))))




# Setting all handlers


oscserver.addMsgHandler( "/on", on )
oscserver.addMsgHandler( "/off", off )
oscserver.addMsgHandler("default", handler)
oscserver.addMsgHandler( "/quit", quit )
oscserver.addMsgHandler( "/padmode", padmode )
oscserver.addMsgHandler( "/noteon", noteon )
oscserver.addMsgHandler( "/noteoff", noteoff )
oscserver.addMsgHandler( "/gyrosc/gyro", gyro )
oscserver.addMsgHandler( "/point", point )
oscserver.addMsgHandler( "/accxyz", accxyztouchosc )
accxyztouchosc
oscserver.addMsgHandler( "/display/PL", display )


oscserver.addMsgHandler( "/nozoid/X", nozX )
oscserver.addMsgHandler( "/nozoid/Y", nozY )
oscserver.addMsgHandler( "/nozoid/color", nozcolor )
oscserver.addMsgHandler( "/stop/rotation", stoprot )
oscserver.addMsgHandler( "/nozoid/offset", nozoffset )

oscserver.addMsgHandler( "/ai/velocity", AiVelocity )
oscserver.addMsgHandler( "/ai/expressivity", AiExpressivity )
oscserver.addMsgHandler( "/ai/sensibility", AiSensibility )
oscserver.addMsgHandler( "/ai/beauty", AiBeauty )

# Led Handlers

oscserver.addMsgHandler( "/led", led )
oscserver.addMsgHandler( "/led/xy", ledxy )
oscserver.addMsgHandler( "/xy", xy )
oscserver.addMsgHandler( "/allcolorbhor", allcolorbhor )
oscserver.addMsgHandler( "/clsbhor", clsbhor)



