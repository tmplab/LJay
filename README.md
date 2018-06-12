LJay v0.5

By Sam Neurohack, Loloster,

LICENCE : CC BY


A software for Live laser actions : choose what to display, modify parameters with many devices: music (Nozoids), gamepad, midicontroller, smartphone, tablet,...

Needs at least : an etherdream DAC connected to an ILDA laser, RJ 45 IP network

GUIs : TouchOSC, Pure Date patch. You can build your own GUI and send commands to LJay through OSC.

Devices supported : Launchpad mini, LP8, bhoreal, gamepad, smartphone & tablet (OSC gyroscopes, GUI : TouchOSC needed) and any MIDI controller that is recognised by your OS.

Nozosc : Semi modular synthetizers from Nozoids can send 3 of their inner sound curves and be displayed in many ways, i.e VCO 1 on X axis and LFO 2 on Y axis.


To run : 

python main.py 

-i or --iport : port number to listen to (8001 by default)

-o or --oport : port number to send to (8002 by default)

-l or --laser : Last digit of etherdream ip address 192.168.1.0/24 (4 by default)


#
# Features
# 

(Doc in progress)

- "plugins" curve generators support. 

- Automatic Midi devices IN & OUT detection (must be seen by OS)
- Automatic USB enttec PRO DMX interface detection


- OSC to midi bridge (see /note and /cc/number)
- OSC to DMX bridge (see /cc/number)
- Bhoreal and Launchpad device start animation
- Control all leds of Bhoreal and Launchpad


#
# External devices 
#

(Doc in Progress)



#
# Make your own curve generator
#

(Doc in progress)

Duplicate and rename a set file like set0.py (import it in main.py).

Program your own curve :
 
- Generate a point list array.
- Use Laser drawing functions : polyline, line, lineto.
- You can have several drawing functions to draw several objects.


If you need to receive data externally : 

use /nozoid/osc/number value : Store a new value in gstt.osc[number] (number : 0-255)
or program your own OSC commands in bhorosc.py

Add your set and curve in settables (main.py)

Modify in gstt set and curve to run your curve at startup.

#
# LJay OSC commands :
#

# General 

/noteon number velocity   
					Note on sent to laser (see below for notes effects). Noteon can also be send to midi targets if gstt.tomidi is True.
/noteoff number 	Note off is sent only to midi targets.


/accxyz x y z 		TouchOSC gyroscope x assigned to cc 1 and y assigned to cc 2. See below for cc effects.

/gyrosc/gyro x y z  Change 3D rotation angles with gyroscope float values. i.e for GyrOSC iOS app. At this time Z is ignored and Z rotation set to 0

/point x y z 		Set point coordinates for "slave" curve. Need to be changed change to collections deque as in llstr.py

/stop/rotation 		Set all 3D rotations speed and 3D rotation angles to 0

/cc/number value : 	Change the cc with given value. Effect will depend on flags set to True : gstt.todmx (value is forwarded to dmx channel) , gstt.tomidi, gstt.tolaser (center align or curve mode). See cc effects below

/number value : 	switch current displayed curve to value.

/enter : 			should validate previous chosen number 

/clear : 			Clear status widget text.

/quit : 			Do nothing yet


# Colors 

In RGB Color mode (see note effects to switch Color mode)

/red 0 : 			Switch off blue laser.

/red 255 (or >0)  	Switch on blue laser


/green 0 : 			Switch off blue laser

/green 255 (or >0)  Switch on blue laser


/blue 0 : 			Switch off blue laser

/blue 255 (or >0)  Switch on blue laser



# Bhoreal and Launchpad devices

/led led number color : Switch on given led with given color. 

/led/xy  x y color	Switch on led wit x y position to given color.
/xy x y 

/allcolorbhor : 	Switch all Bhoreal Leds with given colour (0-127)

/clsbhor :      	Switch off all bhoreal colors

/padmode : 			Code not available yet in LJay. Different modes available for Bhoreal and Launchpad. "Prompt" = 10 ; "Myxo" = 2 ; "Midifile" = 3


 
# Nozoids synthetizers functions originated by nozosc.py and executed in llstr.py (See Nozosc readme for complete OSC implementation and how to control Nozosc)
	

/nozoid/osc/number value : Store a new value for given oscillator/LFO/VCO

/nozoid/X value 	use given oscillator/LFO/VCO number for X axis. See llstr.py 

/nozoid/Y value 	use given oscillator/LFO/VCO number for Y axis. See llstr.py 

/nozoid/color r g b set current laser color  	

/nozoid/knob/number value : Not used yet

/nozoid/mix/number value : Not used yet

/nozoid/vco/number value : Not used yet

/nozoid/lfo/number value : Not used yet



# Advanced TouchOSC GUI Handlers

/on : 			Accept an advanced GUI with status widget. Automatically get the IP, send status,...

/off : 			Disconnect the advanced GUI

/status text	Display some text on status widget GUI

/control/matrix/Y/X 0 or 1
				First screen ("Control") buttons toggle state : on or off

/pad/rights/note 0 or 1	
				"Pad" screen (launchpad mini simulator screen), right column : Send note on and note off

/pad/tops/cc 0 or 1	
				"Pad" screen top raw : Send CC 0/127

#
# Laser Effects 
#

Note on effects :

0-7 	Curve choice 
8-15 	Set choice
16-23 	Laser choice 
		At this time LJay cannot control directly more than one laser. Therefore at least one LJay has to start in master mode : if you issue a noteon in this laser choice range, all future laser osc commands will be forwarded to the correct LJay for execution.

57 		Color mode : Rainbow 
58 		Color mode : RGB 


CC channel effects (0-127):

1
2

5 
6 


21 		3D projection : FOV
22 		3D projection : Distance

29 		3D Rotation speed X
30 		3D Rotation speed Y
31 		3D Rotation speed Z


#
# Install 
#


Doc in progress

apt install git python-pip libasound2-dev python-dev libpython-dev libjack-dev

pip install pysimpledmx

pip install Cython

pip install mido

pip install python-rtmidi tokenize

pip install pygame, pyserial, pyosc


If you have serial or rtmidi python module, remove them first. 

pip uninstall serial 

pip uninstall rtmidi


# 
# Ether dream configuration
#



This program suppose that the ether dream is configured in a certain way especially for its IP address. Write an autoplay.txt file inside an SD Card within the ether dream DAC, with the following lines you can adjust i.e for pps or fps. Yes, there is a builtin DHCP client in the ether dream DAC but if you run multiple lasers, having a fixed dedicated network makes you focus on laser stuff.

/net/ipaddr 192.168.1.3

/net/netmask 255.255.255.0

/net/gateway 192.168.1.1

/ilda/pps 25000

/ilda/fps 25

About hardware setup, especially if you have several lasers : ILDA cables are insanely expensive. You may consider the Power Over Ethernet 'POE' option. Buy a very small ILDA cable, a POE splitter and connect everything to the ether dream fixed near your laser. You can have then a simple and very long network cable and use a Power Over Ethernet injector or switch closed to the driving computer. Beware some vendors use 24V POE Injector : POE injectors and splitters must match.




