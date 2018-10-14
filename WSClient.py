"""

Bhorosc 8002      -> UI websocket 9999

osframe() listener is here.

by Sam Neurohack 
from /team/laser




	WSClient - WebSocket Client

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

import threading, hashlib, base64
import WSSettings
import WSosc

from WSDecoder import *
from WSController import *

## WebSocket Client Class
#
#  Socket control for a given client.

class WSClient:

	# WSClient connection status

	CONNECTION_STATUS = {
		'CONNECTING': 0x0,
		'OPEN': 0x1,
		'CLOSING': 0x2,
		'CLOSED': 0x3
	}

	## Constructor
	#  @param _WSServer WebSocket Server object attached to client.

	def __init__(self,_WSServer):
		self._WSServer = _WSServer
		self.conn = ''
		self.addr = ''
		self.setStatus('CLOSED')
		self._WSController = WSController(self)

	## Set current connection status
	#  @param status Status of the socket. Can be 'CONNECTING', 'OPEN', 'CLOSING' or 'CLOSED'.

	def setStatus(self, status=''):
		if (status in self.CONNECTION_STATUS):
			self.status = self.CONNECTION_STATUS[status]

	## Test current connection status
	#  @param status Status of the socket. Can be 'CONNECTING', 'OPEN', 'CLOSING' or 'CLOSED'.

	def hasStatus(self, status):
		if (status in self.CONNECTION_STATUS):
			return self.status == self.CONNECTION_STATUS[status]
		return False

	## Real socket bytes reception
	#  @param bufsize Buffer size to return.

	def receive(self, bufsize):
		bytes = self.conn.recv(bufsize)
		if not bytes:
			print 'Client left', repr(self.conn)
			self._WSServer.remove(self)
			self.close()
			return ''
		return bytes

	## Try to read an amount bytes
	#  @param bufsize Buffer size to fill.

	def read(self, bufsize):
		remaining = bufsize
		bytes = ''
		while remaining and self.hasStatus('OPEN'):
			bytes += self.receive(remaining)
			remaining = bufsize - len(bytes)
		return bytes

	## Read data until line return (used by handshake)

	def readlineheader(self):
		line = []
		while self.hasStatus('CONNECTING') and len(line)<1024:
			c = self.receive(1)
			line.append(c)
			#print 'readlineheader: ', line
			if c == "\n":
				break
		return "".join(line)

	## Send handshake according to RFC

	def hanshake(self):
		headers = {}
		# Ignore first line with GET
		line = self.readlineheader()
		while self.hasStatus('CONNECTING'):
			if len(headers)>64:
				raise ValueError('Header too long.')
			line = self.readlineheader()
			if not self.hasStatus('CONNECTING'):
				raise ValueError('Client left.')
			if len(line) == 0 or len(line) == 1024:
				raise ValueError('Invalid line in header.')
			if line == '\r\n':
				break
			# take care with strip !
			# >>> import string;string.whitespace
			# '\t\n\x0b\x0c\r '
			line = line.strip()
			# take care with split !
			# >>> a='key1:value1:key2:value2';a.split(':',1)
			# ['key1', 'value1:key2:value2']
			kv = line.split(':', 1)
			if len(kv) == 2:
				key, value = kv
				k = key.strip().lower()
				v = value.strip()
				headers[k] = v
			else:
				raise ValueError('Invalid header key/value.')
		#print headers

		if not len(headers):
			raise ValueError('Reading headers failed.')
		if not 'sec-websocket-version' in headers:
			raise ValueError('Missing parameter "Sec-WebSocket-Version".')
		if not 'sec-websocket-key' in headers:
			raise ValueError('Missing parameter "Sec-WebSocket-Key".')
		if not 'host' in headers:
			raise ValueError('Missing parameter "Host".')
		if not 'origin' in headers:
			raise ValueError('Missing parameter "Origin".')

		if (int(headers['sec-websocket-version']) != WSSettings.VERSION):
			raise ValueError('Wrong protocol version %s.' % WSSettings.VERSION)

		accept = base64.b64encode(hashlib.sha1(headers['sec-websocket-key'] + '258EAFA5-E914-47DA-95CA-C5AB0DC85B11').digest())

		bytes = ('HTTP/1.1 101 Switching Protocols\r\n'
			'Upgrade: websocket\r\n'
			'Connection: Upgrade\r\n'
			'Sec-WebSocket-Origin: %s\r\n'
			'Sec-WebSocket-Location: ws://%s\r\n'
			'Sec-WebSocket-Accept: %s\r\n'
			'Sec-WebSocket-Version: %s\r\n'
			'\r\n') % (headers['origin'], headers['host'], accept, headers['sec-websocket-version'])

		print '--- HANDSHAKE ---'
		print bytes
		print '-----------------'
		self.send(bytes)

	## Handle incoming datas
	#  @param conn Socket of WebSocket client (from WSServer).
	#  @param addr Adress of WebSocket client (from WSServer).

	def handle(self, conn, addr):
		self.conn = conn
		self.addr = addr
		self.setStatus('CONNECTING')
		
		try:
			self.hanshake()
		except ValueError as error:
			self._WSServer.remove(self)
			self.close()
			raise ValueError('Client rejected: ' + str(error))
		else:
			_WSDecoder = WSDecoder()
			self.setStatus('OPEN')
			while self.hasStatus('OPEN'):

				WSosc.osc_frame()
				try:
					ctrl, data = _WSDecoder.decode(self)
				except ValueError as (closing_code, message):
					if self.hasStatus('OPEN'): # context can change...
						self._WSController.kill(closing_code,'WSDecoder::'+str(message))
					break
				else:
					print '--- INCOMING DATAS ---'
					self._WSController.run(ctrl, data)
					print "INCOMING data : ", data
					#print data

	## Send an unicast frame
	#  @param bytes Bytes to send.

	def send(self,bytes):
		if not self.hasStatus('CLOSED'):
			print '--- SEND UNICAST ---', repr(self.conn), repr(bytes), '[', str(len(bytes)), ']'
			lock = threading.Lock()
			lock.acquire()
			self.conn.send(bytes)
			lock.release()
			print 'unicast send finished'

	## Close connexion (don't forget to remove client from WebSocket Server first !)

	def close(self):
		print '--- CLOSE (WSCLIENT) ---', repr(self.conn)
		if not self.hasStatus('CLOSED'):
			self.setStatus('CLOSED')
			self.conn.close()

