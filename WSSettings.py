"""
	WSSettings - WebSockets Const & Settings for others classes

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

# Protocole version from http://tools.ietf.org/html/rfc6455
VERSION = 13

# Operation codes
CONTINUATION = 0x0
TEXT = 0x1
BINARY = 0x2
CLOSE = 0x8
PING = 0x9
PONG = 0xA

OPCODES = (CONTINUATION, TEXT, BINARY, CLOSE, PING, PONG)

# Closing frame status codes.
NORMAL_CLOSURE =  1000 # \x03\xe8
ENDPOINT_IS_GOING_AWAY =  1001 # \x03\xe9
PROTOCOL_ERROR =  1002 # \x03\xea
UNSUPPORTED_DATA_TYPE =  1003 # \x03\xeb
INVALID_PAYLOAD =  1007 # \x03\xef - INCONSISTENT DATA/TYPE
POLICY_VIOLATION =  1008 # \x03\xf0
MESSAGE_TOO_BIG =  1009 # \x03\xf1
EXTENSION_NOT_FOUND_ON_SERVER =  1010 # \x03\xf2
UNEXPECTED_CONDITION_ENCOUTERED_ON_SERVER =  1011 # \x03\xf3

CLOSING_CODES = (NORMAL_CLOSURE, ENDPOINT_IS_GOING_AWAY, PROTOCOL_ERROR, UNSUPPORTED_DATA_TYPE, INVALID_PAYLOAD, POLICY_VIOLATION, MESSAGE_TOO_BIG, EXTENSION_NOT_FOUND_ON_SERVER, UNEXPECTED_CONDITION_ENCOUTERED_ON_SERVER)

# Remember
# 1005 and 1006 codes are reserved and forbidden
#'NOT_AVAILABLE': 1005,
#'ABNORMAL_CLOSED': 1006,
# 1015 code is reserved and forbidden
#'TLS_HANDSHAKE_ERROR': 1015

