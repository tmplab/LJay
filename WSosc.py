# coding=UTF-8
"""

UI websocket 9999 -> Bhorosc 8001
Bhorosc 8002      -> UI websocket 9999

by Sam Neurohack 
from /team/laser


"""

from OSC import OSCServer, OSCClient, OSCMessage
import socket
import types
from WSEncoder import *
from WSServer import *

# Server : relay OSC message from Bhorosc outport 8002 to UI
#oscIPin = "192.168.1.10"
oscIPin = "127.0.0.1"
oscPORTin = 8002

# Client : relay message from UI to Bhorosc inport 8001
oscIPout = "127.0.0.1"
oscPORTout = 8001

print("")
print("Starting OSCServer...")
print ("Receiving on ", oscIPin, ":",str(oscPORTin))
oscserver = OSCServer( (oscIPin, oscPORTin) )
oscserver.timeout = 0
OSCRunning = True

def handle_timeout(self):
    self.timed_out = True

oscserver.handle_timeout = types.MethodType(handle_timeout, oscserver)


osclientme = OSCClient()
oscmsg = OSCMessage()
osclientme.connect((oscIPout, oscPORTout)) 

#_WSEncoder = WSEncoder()
#_WSServer = WSServer()

# send UI string as OSC message to Bhorosc 8001
# sendme(oscaddress, [arg1, arg2,...])

def sendme(oscaddress,oscargs=''):
        
    oscmsg = OSCMessage()
    oscmsg.setAddress(oscaddress)
    oscmsg.append(oscargs)
    
    print "sending to bhorosc : ",oscmsg
    try:
        osclientme.sendto(oscmsg, (oscIPout, oscPORTout))
        oscmsg.clearData()
    except:
        print ('Connection to myself refused')
        pass
    #time.sleep(0.001)


# default handler : send OSC message from Bhorosc to UI via websocket 9999
def handler(path, tags, args, source):

    oscpath = path.split("/")
    pathlength = len(oscpath)
    print ""
    print "default handler"
    print path, oscpath, args

    # /lstt/number value
    if oscpath[1] == "lstt":
        print "lstt"
        '''
        bytes = myWSEncoder.text(path)
        myWSServer.send(bytes)
        #self._WSClient._WSServer.send(bytes)
        # test ping/pong
        #self.ping()
        '''
    '''
    # /lstt/number value
    if oscpath[1] == "lstt":
        number = int(oscpath[2])
        value = int(args[0])
        gstt.cc[number] = value
    '''


# RAW OSC Frame available ? 
def osc_frame():
    # clear timed_out flag
    print "oscframe"
    oscserver.timed_out = False
    # handle all pending requests then return
    while not oscserver.timed_out:
        oscserver.handle_request()



# Default handler for all incoming message from Bhorosc

oscserver.addMsgHandler("default", handler)
