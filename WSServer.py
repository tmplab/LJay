"""

UI websocket 9999 -> Bhorosc 8001
Bhorosc 8002      -> UI websocket 9999


by Sam Neurohack 
from /team/laser



	WSServer - WebSocket Server library for Python

	Copyright (C) 2012 Jean Luc Biellmann (contact@alsatux.com)

	Widely inspired from:
	WebSocket client library for Python - Hiroki Ohtani(liris) - 2010

	This library is free software; you can redistribute it and/or
	modify it under the terms of the GNU Lesser General Public
	License as published by the Free Software Foundation; either
	version 2.1 of the License, or (at your option) any later version.

	This library is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
	Lesser General Public License for more details.

	You should have received a copy of the GNU Lesser General Public
	License along with this library; if not, write to the Free Software
	Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""

import socket, threading, string, time

from WSClient import *

## WebSocket Server Class
#
#  Contains the main thread

class WSServer:

	def __init__(self):
		self.clients = []
		self.s = ''
		self.listening = False

	## Start server
	#  @param host WebSocket server or ip to join. Default is localhost.
	#  @param host port to join. Default is 9999.
	#  @param maxclients Max clients which can connect at the same time. Default is 20.

	def start(self, host='localhost', port=9999, maxclients=20):
		self.s = socket.socket()
		self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.s.bind((host,port))
		self.s.listen(1)
		print 'Server started !'
		print 'Press Ctrl+C to quit'
		self.listening = True
		while self.listening:

			conn, addr = self.s.accept()
			print 'New client host/address:', addr
			if len(self.clients) == maxclients:
				print 'Too much clients - connection refused:', repr(conn)
				conn.close()
			else:
				_WSClient = WSClient(self)
				self.clients.append(_WSClient)
				print 'Total Clients:', str(len(self.clients))
				threading.Thread(target = _WSClient.handle, args = (conn,addr)).start()

	## Send a multicast frame
	#  @param bytes Bytes to send.

	def send(self, bytes):
		print '-- SEND MULTICAST ---', repr(bytes)
		for _WSClient in self.clients:
			_WSClient.send(bytes)
		print 'multicast send finished'

	## Stop all WSClients

	def stop(self):
		self.listening = False
		while (len(self.clients)):
			self.clients.pop()._WSController.kill()
		self.s.close()
		print '--- THAT''S ALL FOLKS ! ---'

	## Remove a WSClient from clients list
	#  @param _WSClient WSClient object to remove from the clients list

	def remove(self,_WSClient):
		if _WSClient in self.clients:
			print 'client left:', repr(_WSClient.conn)
			self.clients.remove(_WSClient)














