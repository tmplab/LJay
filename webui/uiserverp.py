# coding=UTF-8
"""

webUI server Multilaser and redis style.

Dac Status (redis) -> UI websocket 9001
UI websocket 9001 -> Bhorosc 8001
Bhorosc 8002      -> UI websocket 9001

by Sam Neurohack 
from /team/laser

"""


from OSC import OSCServer, OSCClient, OSCMessage
from websocket_server import WebsocketServer
#import socket
import types, thread, time
import redis
import argparse
import ../gstt

print ""
print ""
print "WebUI Server. Multilaser and redis style."
print ""
print "Help for command arguments : --help"
print "Arguments parsing if needed..."
argsparser = argparse.ArgumentParser(description="LJay WebUI server. Multilaser and redis style with automatic DAC status push")
argsparser.add_argument("-l","--lasernumber",help="How many Etherdream are available for Automatic status report (3 by default)",type=int)
argsparser.add_argument("-v","--verbose",help="Verbose level. May decrease rendering quality (0 by default)",type=int)
argsparser.add_argument("-r","--redisIP",help="This computer IP address to bind ('127.0.0.1' by default)",type=str)
argsparser.add_argument("-b","--bhoroscIP",help="Computer IP running bhorosc ('127.0.0.1' by default)",type=str)
argsparser.add_argument("-n","--nozoscIP",help="Computer IP running Nozosc ('127.0.0.1' by default)",type=str)

args = argsparser.parse_args()


if args.verbose != None:
	debug = args.verbose
else:
	debug = 0

if args.redisIP  != None:
	serverIP = args.redisIP
else:
	serverIP = '127.0.0.1'

if args.bhoroscIP  != None:
	bhoroscIP = args.bhoroscIP
else:
	bhoroscIP = '127.0.0.1'

if args.nozoscIP  != None:
	nozoscIP = args.nozoscIP
else:
	nozoscIP = '127.0.0.1'

if args.lasernumber != None:
	LaserNumber = args.lasernumber
else:
	LaserNumber = 3


# Websocket listening port
wsPORT = 9001

# With Bhorosc
# OSC Server : relay OSC message from Bhorosc outport 8002 to UI
#oscIPin = "192.168.1.10"
bhoroscIPin = serverIP
bhoroscPORTin = 8002

# OSC Client : relay message from UI to Bhorosc inport 8001
bhoroscIPout = bhoroscIP 
bhoroscPORTout = 8001


# With Nozosc
# OSC Client : relay message from UI to Nozosc inport 8003
NozoscIPout = nozoscIP
NozoscPORTout = 8003


# 
# OSC part
# 

print("")
print("Starting OSCServer...")
print ("Receiving on ", bhoroscIPin, ":",str(bhoroscPORTin))
oscserver = OSCServer( (bhoroscIPin, bhoroscPORTin) )
oscserver.timeout = 0
OSCRunning = True

def handle_timeout(self):
	self.timed_out = True

oscserver.handle_timeout = types.MethodType(handle_timeout, oscserver)

osclientbhorosc = OSCClient()
oscmsg = OSCMessage()
osclientbhorosc.connect((bhoroscIPout, bhoroscPORTout)) 

# send UI string as OSC message to Bhorosc 8001
# sendbhorosc(oscaddress, [arg1, arg2,...])

def sendbhorosc(oscaddress,oscargs=''):
		
	oscmsg = OSCMessage()
	oscmsg.setAddress(oscaddress)
	oscmsg.append(oscargs)
	
	#print ("sending to bhorosc : ",oscmsg)
	try:
		osclientbhorosc.sendto(oscmsg, (bhoroscIPout, bhoroscPORTout))
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
	
	#print ("sending to nozosc : ",oscmsg)
	try:
		osclientnozosc.sendto(oscmsg, (NozoscIPout, NozoscPORTout))
		oscmsg.clearData()
	except:
		print ('Connection to nozosc refused : died ?')
		sendWSall("/on 0")
		sendWSall("/status No Nozosc ")
		pass
	#time.sleep(0.001)


# OSC default path handler : send OSC message from Bhorosc 8002 to UI via websocket 9001
def handler(path, tags, args, source):

	oscpath = path.split("/")
	pathlength = len(oscpath)
	if debug >0:
		print ""
		print "default handler"
		print "Bhorosc said : ", path, oscpath, args
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



# OSC Thread. Bhorosc handler and Automated status sender to UI.
def osc_thread():

	print "Launching Automatic Dac status and bhorosc forwarder."
	print "Will use Redis server IP ", serverIP 

	r = redis.StrictRedis(host=serverIP, port=6379, db=0)
	print "Connection to redis server.."
	print "Running..."

	while True:
		try:
			while True:

				time.sleep(1)
				osc_frame()

				
				for laserid in range(0,LaserNumber):           # Laser not used -> led is not lit

					lstt = r.get('/lstt/'+ str(laserid))
					#print "laserid", laserid,"lstt",lstt
					if lstt == "0":                              # Dac IDLE state(0) -> led is blue (3)
						sendWSall("/lstt/" + str(laserid) + " 3")
					if lstt == "1":                              # Dac PREPARE state (1) -> led is cyan (2)
						sendWSall("/lstt/" + str(laserid) + " 2")
					if lstt == "2":                              # Dac PLAYING (2) -> led is green (1)
						sendWSall("/lstt/" + str(laserid) + " 1")
				
					# This is used not working : lack never change. Todo : retest.
					lack= r.get('/lack/'+str(laserid))
					#print "laserid", laserid,"lack",lack
					if lack == 'a':                             # Dac sent ACK ("a") -> led is green (1)
						sendWSall("/lack/" + str(laserid) +" 1")
					if lack == 'F':                             # Dac sent FULL ("F") -> led is orange (5)
						sendWSall("/lack/" + str(laserid) +" 5")
					if lack == 'I':                             # Dac sent INVALID ("I") -> led is yellow (4)
						sendWSall("/lack/" + str(laserid)+" 4")
					#print lack
					
					if lack == "64" or lack =="35":    		  # no connection to dac -> leds are red (6)
						sendWSall("/lack/" + str(laserid) + " 0")   
						sendWSall("/lstt/" + str(laserid) + " 0")  
						#sendWSall("/lstt/" + str(laserid) + " 0")  
						sendWSall("/points/" + str(laserid) + " 0")
						
					else:
						# last number of points sent to etherdream buffer
						sendWSall("/points/" + str(laserid) + " " + str(r.get('/cap/'+str(laserid))))

					#sendWSall("/plframe/" + str(laserid) ) # + " " + str(r.get('/pl/'+str(laserid))))

				# WIP Too much packets -> flood webUI : Draw all PL point lists in JS canvas in WebUI
				
				'''
				for pl in range(0,1):   
					bhorosc.sendosc("/plframe/" + str(pl),"")
					for plpoint in range(0,len(gstt.PL[pl])):
						bhorosc.sendosc("/plpoint/" + str(pl),"")
				'''



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
	if debug >0:
		print("WS Client(%d) said: %s" % (client['id'], message))
	oscpath = message.split(" ")
	
	# current UI has no dedicated off button so /on 0 trigs /off to bhorosc
	if oscpath[0] == "/on":
		if oscpath[1] == "1":
			sendbhorosc("/on")
		else:
			sendbhorosc("/off")
	else:   
		print "sending to bhorosc",oscpath[0],oscpath[1]
		sendbhorosc(oscpath[0],oscpath[1])
	
	# if needed a loop back : WS Client -> server -> WS Client
	#sendWSall("ws"+message)


def handle_timeout(self):
	self.timed_out = True


def sendWSall(message):
	if debug >0:
		print("WS sending %s" % (message))
	server.send_message_to_all(message)
	
	
# Launch OSC thread listening to Bhorosc
thread.start_new_thread(osc_thread, ())

# Default OSC handler for all incoming message from Bhorosc
oscserver.addMsgHandler("default", handler)

# Websocket startup
print "ws Server at :", serverIP, "port :",wsPORT

server = WebsocketServer(wsPORT,host=serverIP)
#print server
server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
server.run_forever()
