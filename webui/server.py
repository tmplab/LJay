# coding=UTF-8
"""

UI websocket 9999 -> Bhorosc 8001
Bhorosc 8002      -> UI websocket 9999

by Sam Neurohack 
from /team/laser

"""


from OSC import OSCServer, OSCClient, OSCMessage
from websocket_server import WebsocketServer
#import socket
import types, thread, time

# Websocket listening port
wsPORT = 9001


# With Bhorosc
# OSC Server : relay OSC message from Bhorosc outport 8002 to UI
#oscIPin = "192.168.1.10"
oscIPin = "127.0.0.1"
oscPORTin = 8002

# OSC Client : relay message from UI to Bhorosc inport 8001
oscIPout = "127.0.0.1"
oscPORTout = 8001


# With Nozosc
'''
# OSC Server : relay OSC message from Bhorosc outport 8002 to UI
#oscIPin = "192.168.1.10"
oscIPin = "127.0.0.1"
oscPORTin = 8004
'''
# OSC Client : relay message from UI to Nozosc inport 8003
NozoscIPout = "127.0.0.1"
NozoscPORTout = 8003

# 
# OSC part
# 

print("")
print("Starting OSCServer...")
print ("Receiving on ", oscIPin, ":",str(oscPORTin))
oscserver = OSCServer( (oscIPin, oscPORTin) )
oscserver.timeout = 0
OSCRunning = True

def handle_timeout(self):
    self.timed_out = True

oscserver.handle_timeout = types.MethodType(handle_timeout, oscserver)

osclientbhorosc = OSCClient()
oscmsg = OSCMessage()
osclientbhorosc.connect((oscIPout, oscPORTout)) 

# send UI string as OSC message to Bhorosc 8001
# sendbhorosc(oscaddress, [arg1, arg2,...])

def sendbhorosc(oscaddress,oscargs=''):
        
    oscmsg = OSCMessage()
    oscmsg.setAddress(oscaddress)
    oscmsg.append(oscargs)
    
    print ("sending to bhorosc : ",oscmsg)
    try:
        osclientbhorosc.sendto(oscmsg, (oscIPout, oscPORTout))
        oscmsg.clearData()
    except:
        print ('Connection to bhorosc refused : died ?')
        sendWSall("/on 0")
        sendWSall("/status NoLJay")
        pass
    #time.sleep(0.001)


# send UI string as OSC message to Nozosc 8003
# sendnozosc(oscaddress, [arg1, arg2,...])

def sendnozosc(oscaddress,oscargs=''):
        
    oscmsg = OSCMessage()
    oscmsg.setAddress(oscaddress)
    oscmsg.append(oscargs)
    
    print ("sending to nozosc : ",oscmsg)
    try:
        osclientnozosc.sendto(oscmsg, (NozoscIPout, NozoscPORTout))
        oscmsg.clearData()
    except:
        print ('Connection to nozosc refused : died ?')
        sendWSall("/on 0")
        sendWSall("/status No Nozosc ")
        pass
    #time.sleep(0.001)


# OSC default path handler : send OSC message from Bhorosc to UI via websocket 9999
def handler(path, tags, args, source):

    oscpath = path.split("/")
    pathlength = len(oscpath)
    #print ""
    #print "default handler"
    #print "Bhorosc said : ", path, oscpath, args
    sendWSall(path + " " + str(args[0]))
    '''
    # /lstt/number value
    if oscpath[1] == "lstt":
        sendWSall(path + " " + str(args[0]))
    # /status string
    if oscpath[1] == "status":
        sendWSall(path + " " + str(args[0]))
    '''



# RAW OSC Frame available ? 
def osc_frame():
    # clear timed_out flag
    oscserver.timed_out = False
    # handle all pending requests then return
    while not oscserver.timed_out:
        oscserver.handle_request()

# OSC thread listening to Bhorosc
def osc_thread():
    while True:
        try:
            while True:
               time.sleep(0.006)
               osc_frame()

        except Exception as e:
            import sys, traceback
            print '\n---------------------'
            print 'Exception: %s' % e
            print '- - - - - - - - - - -'
            traceback.print_tb(sys.exc_info()[2])
            print "\n"

#
# Websocket part
# 

# Called for every WS client connecting (after handshake)
def new_client(client, server):
    print("New WS client connected and was given id %d" % client['id'])
    sendWSall("/status Hello %d" % client['id'])

# Called for every WS client disconnecting
def client_left(client, server):
	print("WS Client(%d) disconnected" % client['id'])


# Called when a WS client sends a message
def message_received(client, server, message):
	if len(message) > 200:
		message = message[:200]+'..'
	print("WS Client(%d) said: %s" % (client['id'], message))
	oscpath = message.split(" ")
	
	# current UI has no dedicated off button so /on 0 trigs /off to bhorosc
	if oscpath[0] == "/on":
		if oscpath[1] == "1":
			sendbhorosc("/on")
		else:
			sendbhorosc("/off")
	else:	
		sendbhorosc(oscpath[0],oscpath[1])
	
	# if needed a loop back : WS Client -> server -> WS Client
	#sendWSall("ws"+message)

def handle_timeout(self):
    self.timed_out = True

def sendWSall(message):
    #print("WS sending %s" % (message))
    server.send_message_to_all(message)
    
    
# Launch OSC thread listening to Bhorosc
thread.start_new_thread(osc_thread, ())

# Default OSC handler for all incoming message from Bhorosc
oscserver.addMsgHandler("default", handler)

# Websocket startup

server = WebsocketServer(wsPORT)
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
server.run_forever()
