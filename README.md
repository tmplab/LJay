LJay v0.7.0

By Sam Neurohack, Loloster, Cocoa

LICENCE : CC BY



![LJay](http://www.teamlaser.fr/thsf/images/fulls/THSF9-33.jpg)

A software for Live laser actions with support for up to 4 lasers 

Live modifications with many devices: music (Nozoids), gamepad, midicontroller, smartphone, tablet,...

Needs at least : an etherdream DAC connected to an ILDA laser, RJ 45 IP network (gigabits only !!  no wifi, 100 mpbs doesn't work well with several lasers)

GUIs : WebUI, TouchOSC, Pure Data patch. You can build your own GUI and send/get commands to/from LJay through OSC. Attention : the Pure Data patch works with PD-extended 0.43. Any contribution for whatever "better" Pure Data version are welcome.

Devices supported : Launchpad mini, LP8, enttec DMX PRO, bhoreal, gamepad, smartphone & tablet (with OSC like gyroscopes) and any MIDI controller that is recognised by your OS.

Nozosc : Semi modular synthetizers from Nozoids can send a lot of their inner sound curves and be displayed in many ways, i.e VCO 1 on X axis and LFO 2 on Y axis.

You can also send OSC commands to a video, music,... external software to trigger what you want.


To run one laser style : 

python main.py 

use --help for all arguments


To run multilasers, a server approach is based on redis. One process per etherdream is spawn to retrieve the given point list from redis, warp, resample and manage the given etherdream DAC dialog.

Say the server computer IP is 192.138.1.13, the client computer that run LJ is 192.168.1.52 

On the server computer :
edit /etc/redis/redis.conf or redis-server --slaveof 192.168.1.13 6379 &
python serverp.py -r 192.168.1.13
cd webui/
python uiserverp.py -r 192.168.1.13 -b 192.168.1.52

on the client computer for all features :
python mainp.py -r 192.168.1.13

to just generate and send list points
node testredis.js

to monitor redis server :
redis-cli -h 192.168.1.13 monitor

#
# Features among many others.
# 

(Doc in progress)

- "plugins" "curve" generators support. 
- Automatically hook to Midi devices IN & OUT seen by OS. Very cool : LJay can script or be scripted by a midi device : Triggering different musics at given moments,... or in opposite, you can make a midi file with an external midi sequencer to script/trigger laser effects.
- Automatic USB enttec PRO DMX interface detection
- OSC server. Very cool : LJay can also script or be scripted in OSC with an OSC sequencer like Vezer.
- OSC to midi bridge (see /note and /cc/number)
- OSC to DMX bridge (see /cc/number)
- Bhoreal and Launchpad device start animation
- Control all leds of Bhoreal and Launchpad through midi.
- Multi lasers. 
- Interactive (mouse style) warp correction (set 1 curve 1) for each laser.
- Interactive (mouse style) any shape correction (set 1 curve 0). The shape point list must be defined in a "screen". See configuration file example : setamiral.conf
- rPolyline draw function (r stand for relative) with built in end modifications like rotation, resize, position (and projection but not yet). Points must be centered around 0,0. * Easy way to build your vizualisation : generate each part around 0,0 and use rPolyline to display/resize it at some position. Repeat for all your vizualisation parts. *
- Support openpose json ! display human skeleton animation see setamiral or set 0 Curve 9. Openpose data must be computed around 0,0 ()
- Multiple openpose animations on different lasers, see setamiral.py
- Can control Resolume Arena video software through OSC, like : bhorosc.sendresol("/layer1/clip1/connect",1) 
- Integrated sawtooth, sine and square generator. See set0
- A multi laser example : display solar planet positions at anytime, see Astro() (set 0 Curve 7). As Astro is not necessary and needs a big download, to use it you need to uncomment astro init lines in set0 and follow install instructions. A simplier multilaser example is in setexample.py
- Web ui !! (start server.py from webui directory). This "server" is basically a OSC/websocket bridge. Websocket side talks to webui index.html page. OSC side talks to LJay (bhorosc.py) and Nozosc. All OSC specs are not fully supported.
- Status every 0.5 seconds : every etherdream DAC state, number of buffer points sent,...
- "Optimisation" points automatically added can be changed live, for glitch art. Search "glitch" in gstt.py
- D key will kind of cycle PL in simulator. buggy
- redis server version : Sending points is now dead simple in many langages (add all points coordinates in one string and send it to redis server). Simple keys to exchange data (i.e "/pl/0" is the laser 0 point list).   
- Laser sharing ! In a coding event like demo party the server version, it's a five minutes learning process. Testredis.js has the code to draw some 

#
# External devices 
#

(Doc in Progress)

- LPD8 : A config file is included.
- enttec USB pro
- LaunchPad mini
- Bhoreal
- Joypads : Joypads are detected and read by pygame. You need to adapt the button mapping to your specific gamepad in the code. Search "joypad" in setexample.py




#
# Make your own set and curves.
#

(Doc in progress)

Introduction :
--------------

A "Curve" is actually more a scene/mode, wich must generate all necessary pointlists ("PL") for *all needed lasers*. It's your main drawing function.

A "Set" is a collection of Curves, like a MIDI bank (="Set") has different programs (="Curve"). For the moment there is 8 Sets (0-7) of 8 Curves (0-7). You can actually code as many Curves you want in a Set, the 8 limit is for built in support of the web UI, Bhoreal device,... 

In each Set, Curve 0 is reserved for interactive settings modifications : trapezoidal corrections = "Warp edit mode" and  
 "Windows edit mode" to map custom shapes with mouse.

So your Curve numbers will be 1+. 


Use setexample.py (it is already imported in main.py as Set 4).

Check if your set and all your curves are in settables (main.py)

Use a conf file like setexample.conf, check in gstt.py if Configname use it. The conf file tells LJay what Set/Curve should run at launch. The PL to display in the simulator at first is : simuPL in gstt or a command line argument.

You run with 

python main.py

Be sure to check command arguments : python main.py --help

LJay is meant for Live, so a lot of parameters can be changed via OSC/midi, webUI,...



Program your own "Curve" :
-------------------------

- Read the Introduction part in this readme.
- Carefully read all comments in setexample.py
- Generate at least one point list array (say a circle). 
- Feed your point list array to "drawing functions" : rpolyline, polyline, line, lineto.
- You can have several drawing functions to draw several objects in one big "Point List". It's like building a frame. 
- Once you called all necessary drawing functions, don't forget to feed the result to arrays used by automatic lasers handling functions. If you're building big "Point List" 0 :

gstt.PL[0] = fwork.LinesPL(0)

- One laser takes one big "Point List" PL . All lasers can draw the same PL or different ones, see pl in setexample.conf file. 
- There is many other examples in set0, set1, setamiral,...


To Launch : 
----------

- You can choose which big "Point List" the pygame simulator will show you. Use -d argument.
- Typically to launch say the curve 1 of set 4 and simulator displaying the big "Point List" 0 :

python main.py -s 4 -c 1 -d 0


If you need to receive data externally : 

use /nozoid/osc/number value : Get the new value in gstt.osc[number] (number : 0-255)
or program your own OSC commands in bhorosc.py



Joypads :
---------

You need to decide what to do with joypads axis, hat, buttons. See joypads() in setexample.py. To adapt pygame button numbers to your gamepad use :

python joys.py




"Shapes" :
----------

"Shapes" are mouse editable areas i.e you make a flipper on a building and want something happen with the building windows. "Shapes" are the list of points you see at the beginning of conf file. "Shapes" are grouped in "Screens" that will be displayed by a given laser. See curve 0 in setexample.py
Again "Shapes" are only mousely editable list of points : you can display them or not. 



#
# Install 
#


(Doc in progress)

If you have serial or rtmidi python module, remove them first. 


apt install git python-pip 

pip uninstall serial 

pip uninstall rtmidi

git clone https://github.com/ptone/pyosc --depth 1 /tmp/pyosc && cd /tmp/pyosc && sudo ./setup.py install 

pip install libasound2-dev python-dev libpython-dev libjack-dev

pip install pysimpledmx

pip install numpy

pip install scipy

pip install Cython

pip install mido

pip install python-rtmidi tokenize


Be aware : LJay is tested with pygame 1.9. A long goal is to remove pygame dependancy not support whatever version. 

pip install pygame, pyserial, pyosc


For multilasers a multiprocessed version use redis 

pip install redis

# Last 2, only if you want to use Astro example.

pip install jplephem

wget http://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/de430.bsp


#
# Todo
#

(Doc in Progress)

- Find 3D rotations matrices and 2 projections, test speed / normal algo with algotest.py
- Smaller cpu footprint (compute only when something has changed,...)
- kpps live modification for glitch art.
- Improve Bhoreal & LaunchPad inputs 
- Tags for automatic laser load/ balancing
- Texts : multilasers support, more fonts (See setai/composer )
- Improve WebUI with simulator.
- tomidi should not disable other targets.
- Warp corrections should not used warpdestinations default values in conf file.
- Read and play midifile.
- Remove snap video pose estimation dependancy



#
# LJay OSC commands :
#

# General 

/noteon number velocity   
					: Note on sent to laser (see Midi below for notes effects). Noteon can also be send to midi targets if gstt.tomidi is True, but this disable all other targets for the moment. Todo.

/noteoff number 	 : Note off is sent only to midi targets.


/accxyz x y z 		: TouchOSC gyroscope x assigned to cc 1 and y assigned to cc 2. See Midi below for cc effects.

/gyrosc/gyro x y z  : Change 3D rotation angles with gyroscope float values. i.e for GyrOSC iOS app. At this time Z is ignored and Z rotation set to 0

/point x y z 		: Set point coordinates for "slave" curve. Need to be changed change to collections deque as in llstr.py

/stop/rotation 		: Set all 3D rotations speed and 3D rotation angles to 0

/cc/number value : 	Change the cc with given value. Effect will depend on flags set to True : gstt.todmx (value is forwarded to dmx channel) , gstt.tomidi, gstt.tolaser (center align or curve mode). See cc effects below

/number value : 	switch current displayed curve to value.

/quit : 			Do nothing yet


# Laser Control


/display number	: Select what point list (PL) is displayed by simulator


/swap/X/lasernumber value (0 or 1) 
					: switch on and off general X inversion on given laser
	
/swap/Y/lasernumber value (0 or 1) 
					: switch on and off general Y inversion on given laser


/loffset/X/lasernumber value
					: Move X center on given laser of value pixels

/loffset/Y/lasernumber value
					: Move Y center on given laser of value pixels


/scale/X/lasernumber value
					: Stretch laser display of given laser of value

/scale/Y/lasernumber value
					: Stretch laser display of given laser of value


/ip/lasernumber IP
					: Assign a new etherdream (by its IP adress) for given laser number 

/angle/lasernumber value 
					: Change geometric angle correction for given laser number by computing a new homgraphy

/intens/lasernumber value 
					: Assign a new beam intensity for given laser (todo : if etherdream can actually change it) 

/grid/lasernumber value (0 or 1)
					: Toggle a grid display for given laser 

/mouse/lasernumber value (0 or 1) 
					: Toggle the mapping function for given laser


# Colors 

For currently selected laser and in RGB Color mode (see below MIDI notes effects to switch Color mode and "current" laser selection)

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



Functions originated by nozosc.py and executed in llstr.py (See Nozosc readme for complete OSC implementation and how to control Nozosc). A new firmware by loloster is mandatory for OCS 2 (https://github.com/loloster/ocs-2) and MMO3 (https://github.com/loloster/mmo-3). "curve" means on of the 4 curves managed by nozosc. setllstr.py as differents Set/Curve generator called by LJay that displays these 4 "curves";
	

/nozoid/osc/number value : Store a new value for given oscillator/LFO/VCO

/nozoid/X value curve 	 : Use given oscillator/LFO/VCO number as X axis for given curve . See llstr.py 

/nozoid/Y value curve	 : use given oscillator/LFO/VCO number for Y axis for given curve. See llstr.py 

/nozoid/color r g b curve : set current laser color for given curve

/nozoid/knob/number value : Not used yet

/nozoid/mix/number value : Not used yet

/nozoid/vco/number value : Not used yet

/nozoid/lfo/number value : Not used yet



# GUI

![Advanced Gui](http://www.teamlaser.fr/mcontroller.png)

/on : 			Accept a GUI with status widget. Automatically get its IP, send status,...

/off : 			Disconnect the GUI

/status text	Display some text on status widget GUI

TouchOSC GUI button matrix

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

Midi Note : built in midi notes assignation. More : if you hook a midi led matrix like bhoreal, led are updated. See Noteon_Update() in bhorosc.py 

0-7 	Curve choice. Note on 0 to set Curve O, Note on 1 for Curve 1,...

8-15 	Set choice. All happening Live, so as the new Set may not have the same Curve number, changing Set autoselect the builtin "black" curve (-1) as a fallback, so you can safely choose a new Curve in the new Set.
Example : to switch to Set 0, use note on 8. For Set 1 use note on 9,....

16-23 	Laser choice. "Current laser" choice
Example : to switch to Laser 0, use note on 16. For Laser 1 use note on 17,....


24-31   SimuPL choice. Example : to display PL 0 on simulator it's note on 24. To display PL 1 on simulator it's note on 25.... 

57 		Color mode : Rainbow 

58 		Color mode : RGB 


Midi CC channel effects (0-127) built in assignation, *only* if you use built in 3D rotation and 2D projection in your code. You can assign any CC to any function you code. You can get current value in gstt.cc[ccnumber]. See setexample.py

1	  X position

2	  Y position 

5 	  X select for Lissa curves (set curve )

6 	  Y select for Lissa curves (set curve )


21 		3D projection : FOV

22 		3D projection : Distance


29 		3D Rotation speed X

30 		3D Rotation speed Y

31 		3D Rotation speed Z


#
# Resolume Arena commands
#

A dedicated OSC client is built in. To send OSC commands to resolume use something like 

bhorosc.sendresol("/layer1/clip1/connect",1) 

Remember to specify Resolume IP and port in the beginning of bhorosc.py




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


#
# Coordinates if you use the proj() function
#

3D points (x,y,z) has *0,0,0 in the middle* 
A square centered around origin and size 200 (z =0 is added automatically) :
([-200, -200, 0], [200, -200, 0], [200, 200, 0], [-200, 200, 0], [-200, -200, 0])

Pygame screen points are 2D. *0,0 is top left*
with no 3D rotations + 3D -> 2D Projection  + translation to top left:
[(300.0, 400.0), (500.0, 400.0), (500.0, 200.0), (300.0, 200.0), (300.0, 400.0)]


Pygame points with color is fed to laser renderer
[(300.0, 400.0, 0), (500.0, 400.0, 16776960), (500.0, 200.0, 16776960), (300.0, 200.0, 16776960), (300.0, 400.0, 16776960)]


Laser points traced

Because of blanking many points are automatically added and converted in etherdream coordinates system -32765 to +32765 in x and y axis.

16 (-1500.0, 1500.0, 65280, 65280, 0), (-1500.0, 1500.0, 65280, 65280, 0), (-1500.0, 1500.0, 65280, 65280, 0), (-1500.0, 1500.0, 65280, 65280, 0), (-1500.0, 1500.0, 65280, 65280, 0), (-1500.0, 1500.0, 65280, 65280, 0), (-1500.0, 1500.0, 65280, 65280, 0), (-1500.0, 1500.0, 65280, 65280, 0), (-1500.0, 1500.0, 0, 0, 0), (-1500.0, 1500.0, 0, 0, 0), (-1500.0, 1500.0, 0, 0, 0), (-1500.0, 1500.0, 0, 0, 0), (-1500.0, 1500.0, 0, 0, 0), (-1500.0, 1500.0, 0, 0, 0), (-1500.0, 1500.0, 0, 0, 0), (-1500.0, 1500.0, 0, 0, 0)
8 (1500.0, 1500.0, 65280, 65280, 0), (1500.0, 1500.0, 65280, 65280, 0), (1500.0, 1500.0, 65280, 65280, 0), (1500.0, 1500.0, 65280, 65280, 0), (1500.0, 1500.0, 65280, 65280, 0), (1500.0, 1500.0, 65280, 65280, 0), (1500.0, 1500.0, 65280, 65280, 0), (1500.0, 1500.0, 65280, 65280, 0)
8 (1500.0, -1500.0, 65280, 65280, 0), (1500.0, -1500.0, 65280, 65280, 0), (1500.0, -1500.0, 65280, 65280, 0), (1500.0, -1500.0, 65280, 65280, 0), (1500.0, -1500.0, 65280, 65280, 0), (1500.0, -1500.0, 65280, 65280, 0), (1500.0, -1500.0, 65280, 65280, 0), (1500.0, -1500.0, 65280, 65280, 0)
8 (-1500.0, -1500.0, 65280, 65280, 0), (-1500.0, -1500.0, 65280, 65280, 0), (-1500.0, -1500.0, 65280, 65280, 0), (-1500.0, -1500.0, 65280, 65280, 0), (-1500.0, -1500.0, 65280, 65280, 0), (-1500.0, -1500.0, 65280, 65280, 0), (-1500.0, -1500.0, 65280, 65280, 0), (-1500.0, -1500.0, 65280, 65280, 0)
