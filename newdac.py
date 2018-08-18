# j4cDAC test code
#
# Copyright 2011 Jacob Potter
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# coding=UTF-8

import socket
import time
import struct
from gstt import debug, PL
import gstt
import math
from itertools import cycle
from globalVars import *
import pdb


def pack_point(x, y, r, g, b, i = -1, u1 = 0, u2 = 0, flags = 0):
	"""Pack some color values into a struct dac_point.

	Values must be specified for x, y, r, g, and b. If a value is not
	passed in for the other fields, i will default to max(r, g, b); the 
	rest default to zero.
	"""
	
	if i < 0:
		i = max(r, g, b)

	return struct.pack("<HhhHHHHHH", flags, x, y, r, g, b, i, u1, u2)


class ProtocolError(Exception):
	"""Exception used when a protocol error is detected."""
	pass


class Status(object):
	"""Represents a status response from the DAC."""

	def __init__(self, data):
		"""Initialize from a chunk of data."""
		self.protocol_version, self.le_state, self.playback_state, \
		  self.source, self.le_flags, self.playback_flags, \
		  self.source_flags, self.fullness, self.point_rate, \
		  self.point_count = \
			struct.unpack("<BBBBHHHHII", data)

	def dump(self, prefix = " - "):
		"""Dump to a string."""
		lines = [
			""
			"Host ",
			"Light engine: state %d, flags 0x%x" %
				(self.le_state, self.le_flags),
			"Playback: state %d, flags 0x%x" %
				(self.playback_state, self.playback_flags),
			"Buffer: %d points" %
				(self.fullness, ),
			"Playback: %d kpps, %d points played" %
				(self.point_rate, self.point_count),
			"Source: %d, flags 0x%x" %
				(self.source, self.source_flags)
		]
		if debug == 2:
			for l in lines:
				print prefix + l


class BroadcastPacket(object):
	"""Represents a broadcast packet from the DAC."""

	def __init__(self, st):
		"""Initialize from a chunk of data."""
		self.mac = st[:6]
		self.hw_rev, self.sw_rev, self.buffer_capacity, \
		self.max_point_rate = struct.unpack("<HHHI", st[6:16])
		self.status = Status(st[16:36])

	def dump(self, prefix = " - "):
		"""Dump to a string."""
		lines = [
			"MAC: " + ":".join(
				"%02x" % (ord(o), ) for o in self.mac),
			"HW %d, SW %d" %
				(self.hw_rev, self.sw_rev),
			"Capabilities: max %d points, %d kpps" %
				(self.buffer_capacity, self.max_point_rate)
		]
		for l in lines:
			print prefix + l
		if debug == 1:
			self.status.dump(prefix)


class DAC(object):
	"""A connection to a DAC."""

	# "Laser point List" Point generator
	# points are yielded : Getpoints() call n times OnePoint()
	
	def OnePoint(self):
		
		while True:

			#pdb.set_trace()	
			for indexpoint,currentpoint in enumerate(PL[self.PL]):

				xyc = [currentpoint[0],currentpoint[1],currentpoint[2]]
				self.xyrgb = self.EtherPoint(xyc)

				delta_x, delta_y = self.xyrgb[0] - self.xyrgb_prev[0], self.xyrgb[1] - self.xyrgb_prev[1]
				
				#test adaptation selon longueur ligne
				if math.hypot(delta_x, delta_y) < 4000:

					l_steps = [ (1.0, 8)]

				else:
					l_steps = [ (0.25, 3), (0.75, 3), (1.0, 10)]#(0.0, 1),

				for e in l_steps:
					step = e[0]

					for i in xrange(0,e[1]):

						self.xyrgb_step = (self.xyrgb_prev[0] + step*delta_x, self.xyrgb_prev[1] + step*delta_y) + self.xyrgb[2:]		
						yield self.xyrgb_step

				self.xyrgb_prev = self.xyrgb
			

	def GetPoints(self, n):
	

		d = [self.newstream.next() for i in xrange(n)]
		return d

	def EtherPoint(self, xyc):
		
		# compute for a given point, actual coordinates with alignment parameters (center, zoom, axis swap,..) 
		# and rescaled in etherdream coord space

		'''
		Wich one is faster ??
		
		c = xyc[2]
		XX = xyc[0] - screen_size[0]/2
		YY = xyc[1] - screen_size[1]/2

		# Multilaser style
		x = (screen_size[0]/2 + ((XX * math.cos(gstt.finANGLE[self.PL])) - (YY * math.sin(gstt.finANGLE[self.PL]))) - screen_size[0]/2) * gstt.zoomX[self.PL] + gstt.centerX[self.PL]
		y = (screen_size[1]/2 + ((XX * math.sin(gstt.finANGLE[self.PL])) + (YY * math.cos(gstt.finANGLE[self.PL]))) - screen_size[1]/2) * gstt.zoomY[self.PL] + gstt.centerY[self.PL]
		'''

		c = xyc[2]
		XX = xyc[0] - xy_center[0]
		YY = xyc[1] - xy_center[1]
		CosANGLE = math.cos(gstt.finANGLE[self.PL])
		SinANGLE = math.sin(gstt.finANGLE[self.PL])
		# Multilaser style
		x = (xy_center[0] + ((XX * CosANGLE) - (YY * SinANGLE)) - xy_center[0]) * gstt.zoomX[self.PL] + gstt.centerX[self.PL]
		y = (xy_center[1] + ((XX * SinANGLE) + (YY * CosANGLE)) - xy_center[1]) * gstt.zoomY[self.PL] + gstt.centerY[self.PL]
		
		return (x*gstt.swapX[self.PL], y*gstt.swapY[self.PL], ((c >> 16) & 0xFF) << 8, ((c >> 8) & 0xFF) << 8, (c & 0xFF) << 8)


	def read(self, l):
		"""Read exactly length bytes from the connection."""
		while l > len(self.buf):
			self.buf += self.conn.recv(4096)

		obuf = self.buf
		self.buf = obuf[l:]
		return obuf[:l]

	def readresp(self, cmd):
		"""Read a response from the DAC."""
		data = self.read(22)
		response = data[0]
		cmdR = data[1]
		status = Status(data[2:])

#		status.dump()

		if cmdR != cmd:
			raise ProtocolError("expected resp for %r, got %r"
				% (cmd, cmdR))

		if response != "a":
			raise ProtocolError("expected ACK, got %r"
				% (response, ))

		self.last_status = status
		return status

	def __init__(self, host, PL, port = 7765):
		"""Connect to the DAC over TCP."""
		conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		conn.connect((host, port))
		self.conn = conn
		self.buf = ""
		self.PL = PL
		self.xyrgb = self.xyrgb_prev = (0,0,0,0,0)
		self.newstream = self.OnePoint()

		# Read the "hello" message
		first_status = self.readresp("?")
		first_status.dump()

	def begin(self, lwm, rate):
		cmd = struct.pack("<cHI", "b", lwm, rate)
		self.conn.sendall(cmd)
		return self.readresp("b")

	def update(self, lwm, rate):
		cmd = struct.pack("<cHI", "u", lwm, rate)
		self.conn.sendall(cmd)
		return self.readresp("u")

	def encode_point(self, point):
		return pack_point(*point)

	def write(self, points):
		epoints = map(self.encode_point, points)
		cmd = struct.pack("<cH", "d", len(epoints))
		self.conn.sendall(cmd + "".join(epoints))
		return self.readresp("d")

	def prepare(self):
		self.conn.sendall("p")
		return self.readresp("p")

	def stop(self):
		self.conn.sendall("s")
		return self.readresp("s")

	def estop(self):
		self.conn.sendall("\xFF")
		return self.readresp("\xFF")

	def clear_estop(self):
		self.conn.sendall("c")
		return self.readresp("c")

	def ping(self):
		self.conn.sendall("?")
		return self.readresp("?")

	def play_stream(self):

		# First, prepare the stream
		if self.last_status.playback_state == 2:
			raise Exception("already playing?!")
		elif self.last_status.playback_state == 0:
			self.prepare()

		started = 0

		while True:
			
			#pdb.set_trace()
			# How much room?
			cap = 1799 - self.last_status.fullness


			points = self.GetPoints(cap)
			#print points
			if cap < 100:
				time.sleep(0.005)
				cap += 150

#			print "Writing %d points" % (cap, )
			#t0 = time.time()
			self.write(points)
			#t1 = time.time()
#			print "Took %f" % (t1 - t0, )

			if not started:
				self.begin(0, 30000)
				started = 1


def find_dac():
	"""Listen for broadcast packets."""

	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind(("0.0.0.0", 7654))

	while True:
		data, addr = s.recvfrom(1024)
		bp = BroadcastPacket(data)
		
		print "Packet from %s: " % (addr, )
		bp.dump()


