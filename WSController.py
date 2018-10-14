"""
	WSController - WebSocket Controller

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

import WSSettings
import WSosc

from WSEncoder import *

## WebSocket Controller Class
#
#  Here we decide what to do with indoming ctrl/data frames.

class WSController:

	# OPCODE USED
	# 1000: NORMAL_CLOSURE
	# 1011: UNEXPECTED_CONDITION_ENCOUTERED_ON_SERVER

	## Constructor

	def __init__(self,_WSClient):
		self._WSClient = _WSClient

	## Pop n bytes
	#  @param bytes Bytes to shift.
	#  @param n Number if bytes to shift.

	def array_shift(self, bytes, n):
		out = ''
		for num in range(0,n):
			out += bytes[num]
		return out, bytes[n:]

	## Handle incoming datas
	#  @param ctrl Control dictionnary for data.
	#  @param data Decoded data, text or binary.

	def run(self, ctrl, data):

		print '--- CONTROLLER ---', repr(self._WSClient.conn)
		_WSEncoder = WSEncoder()

		# CONTROLS

		if ctrl['opcode'] == 0x9: # PING
			print '--- PING FRAME ---', repr(self._WSClient.conn)
			try:
				bytes = _WSEncoder.pong('Application data')
			except ValueError as error:
				self._WSClient._WSServer.remove(self._WSClient)
				self.kill(1011, 'WSEncoder error: ' + str(error))
			else:
				self._WSClient.send(bytes)

		if ctrl['opcode'] == 0xA: # PONG
			print '--- PONG FRAME ---', repr(self._WSClient.conn)
			if len(data):
				print 'Pong frame datas:', str(data)

		if ctrl['opcode'] == 0x8: # CLOSE
			print '--- CLOSE FRAME ---', repr(self._WSClient.conn)
			self._WSClient._WSServer.remove(self._WSClient)
			# closing was initiated by server
			if self._WSClient.hasStatus('CLOSING'):
				self._WSClient.close()
			# closing was initiated by client
			if self._WSClient.hasStatus('OPEN'):
				self._WSClient.setStatus('CLOSING')
				self.kill(1000, 'Goodbye !')
			# the two first bytes MUST contains the exit code, follow optionnaly with text data not shown to clients
			if len(data) >= 2:
				code, data = self.array_shift(data,2)
				status = ''
				if code in WSSettings.CLOSING_CODES:
					print 'Closing frame code:', code
				if len(data):
					print 'Closing frame data:', data

		# DATAS

		if ctrl['opcode'] == 0x1: # TEXT
			print '--- TEXT FRAME ---', repr(self._WSClient.conn)

			if len(data):

				print "Controller run() data : ", data
				oscpath = data.split(" ")
				print "Sending OSC Message : ", oscpath[0], oscpath[1]
				WSosc.sendme(oscpath[0],oscpath[1])
				try:
					bytes = _WSEncoder.text(data)
				except ValueError as error:
					self._WSClient._WSServer.remove(self._WSClient)
					self.kill(1011, 'WSEncoder error: ' + str(error))
				else:
					#  send incoming message to all clients
					self._WSClient._WSServer.send(bytes)
					# test ping/pong
					self.ping()

		if ctrl['opcode'] == 0x0: # CONTINUATION
			print '--- CONTINUATION FRAME ---', repr(self._WSClient.conn)
			pass

		if ctrl['opcode'] == 0x2: # BINARY
			print '--- BINARY FRAME ---', repr(self._WSClient.conn)
			pass

	## Send a ping

	def ping(self):
		print '--- PING (CONTROLLER) ---'
		if self._WSClient.hasStatus('OPEN'):
			_WSEncoder = WSEncoder()
			try:
				bytes = _WSEncoder.ping('Application data')
			except ValueError as error:
				self._WSClient._WSServer.remove(self._WSClient)
				self.kill(1011, 'WSEncoder error: ' + str(error))
			else:
				self._WSClient.send(bytes)

	## Force to close the connection
	#  @param code Closing code according to RFC. Default is 1000 (NORMAL_CLOSURE).
	#  @param error Error message to append on closing frame. Default is empty.

	def kill(self, code=1000, error=''):
		print '--- KILL (CONTROLLER)  ---', repr(self._WSClient.conn)
		if not self._WSClient.hasStatus('CLOSED'):
			_WSEncoder = WSEncoder()
			data = struct.pack('!H', code)
			if len(error):
				data += error
			print '--- KILL FRAME ---', code, error, repr(self._WSClient.conn)
			try:
				bytes = _WSEncoder.close(data)
			except ValueError as error:
				self._WSClient.close()
			else:
				self._WSClient.send(bytes)
				self._WSClient.close()





