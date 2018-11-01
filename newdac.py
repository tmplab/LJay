#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# -*- mode: Python -*-

'''
LJay v0.7.0

newdac.py
Unhanced version of the threaded etherdream python library from j4cDAC.

LICENCE : CC
Sam Neurohack, pclf



Conversion in etherdream coordinates and geometric corrections 


Call it with a laser number and which point list to draw. Etherdream IP is found in conf file for given laser number

'''

import socket
import time
import struct
from gstt import debug, PL
import gstt
import math
from itertools import cycle
from globalVars import *
import pdb
import ast

import homography
import numpy as np


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
	# each points is yielded : Getpoints() call n times OnePoint()
	
	def OnePoint(self):
		
		while True:

			#pdb.set_trace()	
			for indexpoint,currentpoint in enumerate(PL[self.PL]):

				xyc = [currentpoint[0],currentpoint[1],currentpoint[2]]
				self.xyrgb = self.EtherPoint(xyc)

				delta_x, delta_y = self.xyrgb[0] - self.xyrgb_prev[0], self.xyrgb[1] - self.xyrgb_prev[1]
				
				#test adaptation selon longueur ligne
				if math.hypot(delta_x, delta_y) < 4000:

					# For glitch art : decrease lsteps
					#l_steps = [ (1.0, 8)]
					l_steps = gstt.stepshortline

				else:
					# For glitch art : decrease lsteps
					#l_steps = [ (0.25, 3), (0.75, 3), (1.0, 10)]#(0.0, 1),
					l_steps = gstt.stepslongline

				for e in l_steps:
					step = e[0]

					for i in xrange(0,e[1]):

						self.xyrgb_step = (self.xyrgb_prev[0] + step*delta_x, self.xyrgb_prev[1] + step*delta_y) + self.xyrgb[2:]		
						yield self.xyrgb_step

				self.xyrgb_prev = self.xyrgb
			

	def GetPoints(self, n):
	

		d = [self.newstream.next() for i in xrange(n)]
		#print d
		return d


	# Etherpoint all transform in one matrix, with warp !!
	# xyc : x y color
	def EtherPoint(self,xyc):
	
		c = xyc[2]
		position = homography.apply(gstt.EDH[self.mylaser],np.array([(xyc[0],xyc[1])]))
		#return (-position[0][0], -position[0][1], ((c >> 16) & 0xFF) << 8, ((c >> 8) & 0xFF) << 8, (c & 0xFF) << 8)
		#return (gstt.swapX[self.mylaser] * position[0][0], gstt.swapY[self.mylaser] * position[0][1], ((c >> 16) & 0xFF) << 8, ((c >> 8) & 0xFF) << 8, (c & 0xFF) << 8)
		return (position[0][0],  position[0][1], ((c >> 16) & 0xFF) << 8, ((c >> 8) & 0xFF) << 8, (c & 0xFF) << 8)


	'''
	# Etherpoint Legacy style
	def EtherPoint(self, xyc):
		
		# compute for a given point, actual coordinates with alignment parameters (center, zoom, axis swap,..) 
		# and rescaled in etherdream coord space

		c = xyc[2]
		XX = xyc[0] - xy_center[0]
		YY = xyc[1] - xy_center[1]
		CosANGLE = math.cos(gstt.finANGLE[self.mylaser])
		SinANGLE = math.sin(gstt.finANGLE[self.mylaser])
		# Multilaser style
		x = (xy_center[0] + ((XX * CosANGLE) - (YY * SinANGLE)) - xy_center[0]) * gstt.zoomX[self.mylaser] + gstt.centerX[self.mylaser]
		y = (xy_center[1] + ((XX * SinANGLE) + (YY * CosANGLE)) - xy_center[1]) * gstt.zoomY[self.mylaser] + gstt.centerY[self.mylaser]
		
		return (x*gstt.swapX[self.mylaser], y*gstt.swapY[self.mylaser], ((c >> 16) & 0xFF) << 8, ((c >> 8) & 0xFF) << 8, (c & 0xFF) << 8)
	'''




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
		#print "laser response", self.mylaser, response
		gstt.lstt_dacanswers[self.mylaser] = response
		cmdR = data[1]
		status = Status(data[2:])


		if cmdR != cmd:
			raise ProtocolError("expected resp for %r, got %r"
				% (cmd, cmdR))

		if response != "a":
			raise ProtocolError("expected ACK, got %r"
				% (response, ))

		self.last_status = status
		return status

	def __init__(self, mylaser, PL, port = 7765):
		"""Connect to the DAC over TCP."""
		socket.setdefaulttimeout(2)
		#print "init"
		self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connstatus = self.conn.connect_ex((gstt.lasersIPS[mylaser], port))
		#print "Connection status : ", self.connstatus
		# ipconn state is -1 at startup (see gstt) and modified here
		gstt.lstt_ipconn[mylaser] =  self.connstatus
		self.buf = ""
		self.PL = PL
		self.mylaser = mylaser
		self.xyrgb = self.xyrgb_prev = (0,0,0,0,0)
		self.newstream = self.OnePoint()
		if self.connstatus != 0 and gstt.debug > 0:
			print ""
			print "ERROR connection with laser :", str(mylaser),str(gstt.lasersIPS[mylaser])
			print "first 10 points in PL",self.PL, self.GetPoints(10)

		# Reference points 
		# Read the "hello" message
		first_status = self.readresp("?")
		first_status.dump()
		position = []


	def begin(self, lwm, rate):
		cmd = struct.pack("<cHI", "b", lwm, rate)
		#print "Begin newdac : Laser ",  str(self.mylaser), " PL : ", str(self.PL)

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
		# print last playbaxk state
		#print "Pb : ",self.last_status.playback_state
		if self.last_status.playback_state == 2:
			raise Exception("already playing?!")
		elif self.last_status.playback_state == 0:
			self.prepare()

		started = 0

		while True:

			gstt.lstt_dacstt[self.mylaser] = self.last_status.playback_state
			# pdb.set_trace()
			# How much room?

			cap = 1799 - self.last_status.fullness
			points = self.GetPoints(cap)

			gstt.lstt_points[self.mylaser] = cap 

			#if self.mylaser == 0:
			#print self.mylaser, cap
			if cap < 100:
				time.sleep(0.005)
				cap += 150

#			print "Writing %d points" % (cap, )
			#t0 = time.time()
			self.write(points)
			#t1 = time.time()
#			print "Took %f" % (t1 - t0, )

			if not started:
				self.begin(0, 25000)
				started = 1

# not used in LJay : etherdreams have fixed IP. See conf file
def find_dac():
	"""Listen for broadcast packets."""

	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind(("0.0.0.0", 7654))

	while True:
		data, addr = s.recvfrom(1024)
		bp = BroadcastPacket(data)
		
		print "Packet from %s: " % (addr, )
		bp.dump()
