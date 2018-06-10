
import globalVars
import midi
import time
import rtmidi
from rtmidi.midiutil import open_midiinput 
from threading import Thread
from rtmidi.midiconstants import (CHANNEL_PRESSURE, CONTROLLER_CHANGE, NOTE_ON, NOTE_OFF,
                                  PITCH_BEND, POLY_PRESSURE, PROGRAM_CHANGE)

import bhorosc

from mido import MidiFile
import mido
import sys


is_py2 = sys.version[0] == '2'
if is_py2:
    from Queue import Queue
else:
    from queue import Queue


PadLeds = [0] * 64
PadTops= [0] * 8
PadRights= [0] * 8

# midi notes
LaunchLedMatrix = [(0,1,2,3,4,5,6,7),(16,17,18,19,20,21,22,23),(32,33,34,35,36,37,38,39),(48,49,50,51,52,53,54,55),(64,65,66,67,68,69,70,71),(80,81,82,83,84,85,86,87),(96,97,98,99,100,101,102,103),(112,113,114,115,116,117,118,119)]
# Notes
LaunchRight = (8,24,40,56,72,88,104,120) 
# CC
LaunchTop = (104,105,106,107,108,109,110,111)

def PadNoteOn(note,color):
    (x,y) = BhorIndex(note)
    PadNoteOnXY(x,y,color)

def PadNoteOff(note):
    (x,y) = BhorIndex(note)
    PadNoteOffXY(x,y)

def PadNoteOnXY(x,y,color):
    msg= [NOTE_ON, PadNoteXY(x,y), color]
    #print msg
    midi.send("Launchpad",msg)
    PadLeds[BhorNoteXY(x,y)]=color

    
def PadNoteOffXY(x,y):
    msg= [NOTE_OFF, PadNoteXY(x,y), 0]
    midi.send("Launchpad",msg)
    PadLeds[BhorNoteXY(x,y)]=0
        
def PadNoteXY(x,y):
    note = LaunchLedMatrix[y-1][x-1]
    return note

def PadIndex(note):
    y=note/16
    x=note%16
    return x+1,y+1

def BhorIndex(note):
    y=note/8
    x=note%8
    #print "Note : ",note
    #print "BhorIndex : ", x+1,y+1
    return x+1,y+1

def BhorNoteXY(x,y):
    note = (x -1)+ (y-1) * 8 
    return note

# top raw and right column leds are numbered humanly 1-8. So -1 is for pythonic arrays position 0-7  
def PadTopOn(number,color):
    msg= [CONTROLLER_CHANGE, LaunchTop[number-1], color]
    midi.send("Launchpad",msg)
    PadTops[number-1]=color

def PadTopOff(number):
    msg= [CONTROLLER_CHANGE, LaunchTop[number-1], 0]
    midi.send("Launchpad",msg)
    PadTops[number-1]=0

def PadRightOn(number,color):
    msg= [NOTE_ON, LaunchRight[number-1], color]
    midi.send("Launchpad",msg)
    PadRights[number-1]=color

def PadRightOff(number):
    msg= [NOTE_OFF, LaunchRight[number-1], 0]
    midi.send("Launchpad",msg)   
    PadRights[number-1]=0


#
# LaunchPad start anim
#

# AllColor for bhoreal on given port
def AllColorPad(color):
    
    for led in range(0,64,1):
        PadNoteOn(led,color)
    '''
    for line in LaunchLedMatrix:
        for led in line:
            midiport[port].send_message([NOTE_ON, led, color])
    '''
    for rightled in range(8):
        PadRightOn(rightled+1,color)
    for topled in range(8):
        PadTopOn(topled+1,color)
        #midiport[port].send_message([CONTROLLER_CHANGE, topled, color])

def Cls():

    for led in range(0,64,1):
        PadNoteOff(led)

    '''
    for line in LaunchLedMatrix:
        for led in line:
            midiport[port].send_message([NOTE_OFF, led, 0])
    '''
    for rightled in range(8):
        PadRightOff(rightled+1)
    for topled in range(8):
        PadTopOff(topled+1)
        #midiport[port].send_message([CONTROLLER_CHANGE, topled, 0])

def StartLaunchPad(port):

    #ClsPad(port)
    #time.sleep(0.3)
    AllColorPad(20)
    time.sleep(0.6)
    Cls()
    time.sleep(0.3)

launchqueue = Queue()

#       
# Events from Launchpad Handling
#

# Process events coming from Launchpad in a separate thread.
def LaunchMidinProcess(launchqueue):

    launchqueue_get = launchqueue.get
    
    while True:
    
        msg = launchqueue_get()
        # Note On
        #print msg

        if msg[0]==NOTE_ON:
            #PadLeds[msg[1]]
            #Launch send back note on and off to light up the led.
            (x,y) = PadIndex(msg[1])
            #print x,y
            #print ("Launchpad Button : ", str(msg[1]))

            if x<9:
                msg[1]= BhorNoteXY(x,y)
                print "Pad Matrix : ", msg[1],msg[2]
                midi.NoteOn(msg[1],msg[2])         
                time.sleep(0.1)
                midi.NoteOff(msg[1])

            if x == 9:
                print "Right Button : ", y
                PadRightOn(y,msg[2])
                time.sleep(0.1)
                PadRightOff(y)

        if msg[0]==CONTROLLER_CHANGE:
            print "Pad Top Button : ", str(msg[1]-103)
            PadTopOn(msg[1]-103,msg[2])
            time.sleep(0.1)
            PadTopOff(msg[1]-103)

# LaunchPad Mini call back : new msg forwarded to Launchpad queue 
class LaunchAddQueue(object):
    def __init__(self, port):
        self.port = port
        self._wallclock = time.time()

    def __call__(self, event, data=None):
        message, deltatime = event
        self._wallclock += deltatime
        #print("[%s] @%0.6f %r" % (self.port, self._wallclock, message))
        launchqueue.put(message)
