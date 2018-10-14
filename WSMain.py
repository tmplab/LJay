"""

UI websocket 9999 -> Bhorosc 8001
Bhorosc 8002      -> UI websocket 9999


by Sam Neurohack 
from /team/laser


	WSMain - WebSocket Main

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

"""
SCHEME:

  WSMain (Startup)   incoming datas
    |                       |
    v                       v
WSServer (listen) => WSClient (thread) -> WSDecoder (one per WSClient)
    ^                       ^                  |
    |                       |                  |
    |                       |                  |
    |                       |                  v
    |                       |        	 WSController (one per WSClient)
    |                    unicast               |
    |                       |                  |
    |                       |                  |
    |                       |                  v
    |-------multicast-------|------------- WSEncoder
"""

from WSServer import *

if __name__ == "__main__":
	_WSServer = WSServer()
	try:
		_WSServer.start(host='', port=9999, maxclients=20)
	except (KeyboardInterrupt, SystemExit):
		print '--- KEYBOARD INTERRUPT ---'
		_WSServer.stop()
