TouchOSC myPAD 

OSC Reference 

sending port 8001
Receiving port 8002

Status screen
-------------

/status text

ON/OFF ?
--------

/on 1 or 0
/off 1 or 0
/bhoreal/on 1 or 0    Bhoreal found ? /
/pad/on 1 or 0        Launchpad found ?



My Controller tab
-----------------




LaunchPad tab
-------------



- Top Leds

1/1..........1/8

from left to right :
x = 0 -> off
x = 1 -> on 

/pad/tops/1/(1-8) x



- Right Leds

from top to bottom :
x = 0 -> off
x = 1 -> on 

/pad/rights/1/(8-1) x

8 is on top 1 at bottom

8/1
.
.
.
.
.
.
1/1



- Matrix 

/pad/yx/Y(8-1)/X(1-8) x

Select column Y from top to bottom :
8 -> 1 
Select raw X from left to right :
1 -> 8

8/1..........8/8 
.
.
.
.
.
.
1/1..........1/8




OCS-2 tab
----------

/ocs(MIDI CC number) x

x : float 0 -> 127