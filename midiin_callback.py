#!/usr/bin/env python
#
# test_midiin_callback.py
#
"""Show how to receive MIDI input by setting a callback function."""

from __future__ import print_function

import logging
import sys
import time
from OSC import OSCServer, OSCClient, OSCMessage
import types
import mido
from rtmidi.midiutil import open_midiinput
import socket
from rtmidi.midiconstants import (CHANNEL_PRESSURE, CONTROLLER_CHANGE, NOTE_ON, NOTE_OFF,
                                  PITCH_BEND, POLY_PRESSURE, PROGRAM_CHANGE)

#oscIPout = ""
#oscIPout = "10.255.255.194"
oscIPout = socket.gethostbyname(socket.gethostname())
oscPORTout = 8001
#oscPORTout = 8002


osclient = OSCClient()
oscmsg = OSCMessage()


# sendosc(oscaddress, [arg1, arg2,...])
def sendosc(oscaddress,oscargs):
    
    # also works : osclient.send(OSCMessage("/led", oscargs))

    oscmsg = OSCMessage()
    oscmsg.setAddress(oscaddress)
    oscmsg.append(oscargs)
    
    #print "sending : ", oscmsg
    try:
        osclient.sendto(oscmsg, (oscIPout, oscPORTout))
        oscmsg.clearData()
    except:
        print ('Connection refused at ',oscIPout)
        pass
    #time.sleep(0.001)



log = logging.getLogger('midiin_callback')
logging.basicConfig(level=logging.DEBUG)


class MidiInputHandler(object):
    def __init__(self, port):
        self.port = port
        self._wallclock = time.time()

    def __call__(self, event, data=None):
        message, deltatime = event
        self._wallclock += deltatime
        print("[%s] @%0.6f %r" % (self.port, self._wallclock, message))

        # other midi message          
        if message[0] == CONTROLLER_CHANGE:
            sendosc((''.join(("/cc/",str(int(message[1]))))), int(message[2]))

        # other midi message          
        if message[0] == NOTE_ON:
            sendosc("/noteon", int(message[1]))

        '''
        # other midi message          
        if message[0] == NOTE_OFF:
            sendosc("/noteoff", int(message[1]))
        '''

# Prompts user for MIDI input port, unless a valid port number or name
# is given as the first argument on the command line.
# API backend defaults to ALSA on Linux.
port = sys.argv[1] if len(sys.argv) > 1 else None

try:
    midiin, port_name = open_midiinput(port)
except (EOFError, KeyboardInterrupt):
    sys.exit()

print("Attaching MIDI input callback handler.")
midiin.set_callback(MidiInputHandler(port_name))

print("Entering main loop. Press Control-C to exit.")
try:
    # Just wait for keyboard interrupt,
    # everything else is handled via the input callback.
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print('')
finally:
    print("Exit.")
    midiin.close_port()
    del midiin
