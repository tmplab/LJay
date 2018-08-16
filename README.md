LJay v0.6.2

By Sam Neurohack, Loloster, Cocoa

LICENCE : CC BY



![LJay](http://www.teamlaser.fr/thsf/images/fulls/THSF9-33.jpg)

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
- A multi laser example : display solar planet position is provided see Astro() (set 0 Curve 7). You need python module jplephem and to download de430.bsp : http://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/de430.bsp
- Edit Shapes with mouse



#
# Todo
#

(Doc in Progress)


- Interactive trapezoidal correction via homography matrices for each laser, stored in settings file.
- Smaller cpu footprint (compute only when something has changed,...)
- Tags for automatic laser load/ balancing
- Texts : multilasers support, more fonts (See setai/composer )
- New UI and simulator : web, livecode ?
- Unified settings file, one per set.



#
# External devices 
#

(Doc in Progress)

LPD8 : A config file is included.
Joypads : Xbox style controllers. Joypads are detected and read by pygame, you need to decide what to do with joypads axis, hat, buttons. Example in set1.joypads()



#
# Make your own set.
#

(Doc in progress)

A "Curve" is actually more a mode, wich can generate different pointlists, be an interactive shape modifier,...

A "Set" is a collection of curves

Curve 0 is reserved for interactive settings modifications i.e trapezoidal corrections,...



Duplicate and rename a set file like set0.py (import it in main.py).

Add your set and curves in settables (main.py)

Use command line arguments (-s setnumber -c curvenumber) or modify in gstt Set and Curve.



Program your own "curve" :
 
- Generate at least one point list array. One laser takes one "point list". Any point list can be sent to any laser (= all lasers can draw the same point list or different ones)
- Use Laser "drawing functions" : polyline, line, lineto.
- You can have several drawing functions to draw several objects in one point list.


If you need to receive data externally : 

use /nozoid/osc/number value : Store a new value in gstt.osc[number] (number : 0-255)
or program your own OSC commands in bhorosc.py



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

/quit : 			Do nothing yet

/display/PL	number	Select what point list (PL) is displayed by simulator


# Colors 

In RGB Color mode (see note effects to switch Color mode)

/red 0 : 			Switch off blue laser.

/red 255 (or >0)  	Switch on blue laser


/green 0 : 			Switch off blue laser

/green 255 (or >0)  Switch on blue laser


/blue 0 : 			Switch off blue laser

/blue 255 (or >0)  Switch on blue laser



# Bhoreal and Launchpad devices

![Bhoreal](http://levfestival.com/13/wp-content/uploads/Bhoreal_2.jpg)

/led led number color : Switch on given led with given color. 

/led/xy  x y color	Switch on led with x y position to given color.

/xy x y 

/allcolorbhor : 	Switch all Bhoreal Leds with given colour (0-127)

/clsbhor :      	Switch off all bhoreal leds

/padmode : 			Code not available yet in LJay. Different modes available for Bhoreal and Launchpad. "Prompt" = 10 ; "Myxo" = 2 ; "Midifile" = 3


 

# Nozoids synthetizers 

![Nozoid synthetizer](http://nozoid.com/wp-content/uploads/2017/05/OCS_previus-600x330.png)



Functions originated by nozosc.py and executed in llstr.py (See Nozosc readme for complete OSC implementation and how to control Nozosc). A new firmware by loloster is mandatory for OCS 2 (https://github.com/loloster/ocs-2) and MMO3 (https://github.com/loloster/mmo-3)
	

/nozoid/osc/number value : Store a new value for given oscillator/LFO/VCO

/nozoid/X value 	use given oscillator/LFO/VCO number for X axis. See llstr.py 

/nozoid/Y value 	use given oscillator/LFO/VCO number for Y axis. See llstr.py 

/nozoid/color r g b set current laser color  	

/nozoid/knob/number value : Not used yet

/nozoid/mix/number value : Not used yet

/nozoid/vco/number value : Not used yet

/nozoid/lfo/number value : Not used yet



# Advanced TouchOSC GUI

![Advanced Gui](http://www.teamlaser.fr/mcontroller.png)

/on : 			Accept an advanced GUI with status widget. Automatically get the IP, send status,...

/off : 			Disconnect the advanced GUI

/status text	Display some text on status widget GUI

/clear : 		Clear status widget text.

/enter : 		should validate previous chosen number 


/control/matrix/Y/X 0 or 1
				First screen ("Control") buttons toggle state : on or off

/pad/rights/note 0 or 1	
				"Pad" screen (launchpad mini simulator screen), right column : Send note on and note off

/pad/tops/cc 0 or 1	
				"Pad" screen top raw : Send CC 0/127



#
# Midi commands
#

Midi Note :

0-7 	Curve choice 

8-15 	Set choice

16-23 	Laser choice 


57 		Color mode : Rainbow 

58 		Color mode : RGB 


Midi CC channel effects (0-127) if you use built in 3D rotation and 2D projection in your set.

1	  X position

2	  Y position 

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


(Doc in progress)

If you have serial or rtmidi python module, remove them first. 

pip uninstall serial 

pip uninstall rtmidi


apt install git python-pip libasound2-dev python-dev libpython-dev libjack-dev

pip install pysimpledmx

pip install Cython

pip install mido

pip install python-rtmidi tokenize

pip install pygame, pyserial, pyosc

pip install jplephem

wget http://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/de430.bsp



# 
# Ether dream configuration
#

![Etherdream Laser DAC](https://www.ether-dream.com/ed2-external.jpg)

This program suppose that the ether dream is configured in a certain way especially for its IP address. For ether dream 1 : write an autoplay.txt file inside an SD Card within the ether dream DAC, with the following lines you can adjust i.e for pps or fps. Yes, there is a builtin DHCP client in the ether dream DAC but if you run multiple lasers, having a fixed dedicated network makes you focus on laser stuff.

/net/ipaddr 192.168.1.3

/net/netmask 255.255.255.0

/net/gateway 192.168.1.1

/ilda/pps 25000

/ilda/fps 25

About hardware setup, especially if you have several lasers : ILDA cables are insanely expensive. You may consider the Power Over Ethernet 'POE' option. Buy a very small ILDA cable, a POE splitter and connect everything to the ether dream fixed near your laser. You can have then a simple and very long network cable and use a Power Over Ethernet injector or switch closed to the driving computer. Beware some vendors use 24V POE Injector : POE injectors and splitters must match.




