
import time
from rtmidi.midiconstants import (CHANNEL_PRESSURE, CONTROLLER_CHANGE, NOTE_ON, NOTE_OFF,
                                  PITCH_BEND, POLY_PRESSURE, PROGRAM_CHANGE)

import gstt
import midi
#import bhorosc
#import launchpad

import sys


is_py2 = sys.version[0] == '2'
if is_py2:
    from Queue import Queue
else:
    from queue import Queue



def NoteOnXY(x,y,color):
    #print x,y
    msg = [NOTE_ON, NoteXY(x,y), color]
    midi.send("Bhoreal",msg)
    gstt.BhorLeds[NoteXY(x,y)]=color
    
def NoteOffXY(x,y):
    msg = [NOTE_OFF, NoteXY(x,y), 0]
    midi.send("Bhoreal",msg)
    gstt.BhorLeds[NoteXY(x,y)]=0

# Leds position are humans numbers 1-8. So -1 for pythonic array position 0-7
def NoteXY(x,y):
    note = (x -1)+ (y-1) * 8 
    return note

def Index(note):
    y=note/8
    x=note%8
    #print "Note : ",note
    #print "BhorIndex : ", x+1,y+1
    return x+1,y+1

#    
# Bhoreal Start anim
#

# AllColor for bhoreal on given port

def AllColor(port,color):
    for led in range(0,64,1):
        msg = [NOTE_ON, led, color]
        midi.send("Bhoreal",msg)
 
# Cls for bhoreal on given port

def Cls(port):
    for led in range(0,64,1):
        msg = [NOTE_OFF, led, 0]
        midi.send("Bhoreal",msg)

def StartBhoreal(port):

    Cls(port)
    time.sleep(0.2)
    for color in range(0,126,1):
        AllColor(port,color)
        time.sleep(0.02)
    time.sleep(0.2)
    Cls(port)
#       
# Events from Bhoreal handling
#

# Process events coming from Bhoreal in a separate thread.
def MidinProcess(bhorqueue):

    bhorqueue_get = bhorqueue.get  
    while True:
    
        msg = bhorqueue_get()
        # Note On
        print msg
        if msg[0]==NOTE_ON:
            if gstt.BhorLeds[msg[1]] < 115:
                 gstt.BhorLeds[msg[1]] += 10
                 
            #Bhoreal send back note on and off to light up the led.
            midi.NoteOn(msg[1],gstt.BhorLeds[msg[1]])
            print "Bhoreal Matrix : ", str(msg[1]), str(gstt.BhorLeds[msg[1]])
            time.sleep(0.1)
            midi.NoteOff(msg[1])

bhorqueue = Queue()


# Bhoreal call back : new msg forwarded to Bhoreal queue 
class AddQueue(object):
    def __init__(self, port):
        self.port = port
        self._wallclock = time.time()

    def __call__(self, event, data=None):
        message, deltatime = event
        self._wallclock += deltatime
        #print("[%s] @%0.6f %r" % (self.port, self._wallclock, message))
        bhorqueue.put(message)
 
