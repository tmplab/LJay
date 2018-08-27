# coding=UTF-8
'''
Etat global (anciennement singleton de la classe GameState + autres VARIABLES nécessaires partout)"
'''

from globalVars import *


# How many lasers are connected. Different that "currentlaser" used by bhorosc
LaserNumber = 2


# gstt.Laser select to what laser modifcation will occur.
# Can be changed with /noteon 16-23

Laser = 0

# gstt.simuPL select what point list number to display in pygame simulator
# Can be changed with /noteon 24-31

simuPL = 2

# gstt.laserIPS. Will be overridden by settings.conf values
lasersIPS = ['192.168.1.5','192.168.1.6','192.168.1.3','192.168.1.4']


# gstt.laserPLS : What point list is sent to what laser. 
# ** Will be overridden by settings.conf values **
lasersPLS = [0,0,0,0]
PL = [[],[],[],[]]


EDH = [[], [], [], []]

# gstt.Set select what to Curve Set to display. 
# Can be changed with /noteon 8-15
Set = 1 #nozoid loloster.py


# gstt.Curve select what curve to use in . 
# Can be changed with /noteon 0-7
Curve = 0 #nozmod

ConfigName = "set1.conf"

maxCurvesByLaser = 4


#curveColor = [255,0,0] * maxCurvesByLaser
curveColor = [[0 for _ in range(3)] for _ in range(maxCurvesByLaser)]
colorX = [[255 for _ in range(3)] for _ in range(maxCurvesByLaser)]
colorY = [[255 for _ in range(3)] for _ in range(maxCurvesByLaser)]
offsetX = [0] * maxCurvesByLaser
offsetY = [0] * maxCurvesByLaser
curveNumber = 0
Curve = curveNumber

#curveX = [255,255,255] * maxCurvesByLaser
#curveY = [255,255,255] * maxCurvesByLaser



Mode = 5

point = [0,0,0]

# gstt.colormode select what to display. Can be changed with /noteon 57-64
colormode = 0
color = [255,255,0]
newcolor = 0

surpriseoff = 10
surpriseon = 50
surprisey = -10
surprisex = -10

cc = [0] * 256
lfo = [0] * 10
osc = [0] * 255
oscInUse = [0] * 255
knob = [0] * 33

# Viewer distance (cc 21) 
cc[21]=60
viewer_distance = cc[21] * 8

# fov (cc 22) 
cc[22]= 60
fov = 4 * cc[22]

debug = 0

'''
Also vailable with args : -v Value 

if debug = 1 you get :


if debug = 2 you get :
- dac errors

'''


JumpFlag =0


# nice X (cc 5) Y (cc 6) curve at first
cc[5] = cc[6] = 60

# Dot mode start at middle screen
cc[1] = cc[2] = 63

note = 0
velocity = 0

WingHere = -1
BhorealHere = -1
LaunchHere = -1
BhorLeds = [0] * 64

oscx = 0
oscy = 0
oscz = 0


# Ai Parameters

aivelocity = 0.5
aiexpressivity = 0.5
aisensibility = 0.5
aibeauty =  0.5


# OSC ports
#temporaray fix hack : iport=nozoport
iport = 8001 #LJay (bhorosc) input port
oport = 8002 #LJay (bhorosc) output port
noziport=8003 #nozosc.py receiving commands port
nozoport=8001 #nozosc.py sending port to LJay (main.py)
nozuport=0 #linux serial usb port connecting nozoid devices ACM0 by default


X = [0] * maxCurvesByLaser
Y = [0] * maxCurvesByLaser

# No rotation X (cc 29) Y (cc 30) Z (cc 31)  at first
cc[29] = cc[30] = cc[31] = prev_cc29 = 0
prev_cc29 = prev_cc30 = prev_cc31 = -1

angleX = 0 
angleY = 0
angleZ = 0

tomidi = False
todmx = False
toled = False
tolaser = True
tosynth = False

sernozoid = ""
nozoid = ""
serdmx = ""
newnumber = ""
oldnumber = ""

# will be overrided but settings.conf values.
# legacy one laser only values
centerx = LASER_CENTER_X
centery = LASER_CENTER_Y
zoomx = LASER_ZOOM_X
zoomy = LASER_ZOOM_Y
sizex = LASER_SIZE_X
sizey = LASER_SIZE_Y
finangle = LASER_ANGLE


# multilasers arrays
# will be overrided but settings.conf values.
centerX = [LASER_CENTER_X, LASER_CENTER_X,LASER_CENTER_X,LASER_CENTER_X]
centerY = [LASER_CENTER_Y, LASER_CENTER_Y,LASER_CENTER_Y,LASER_CENTER_Y]
zoomX = [LASER_ZOOM_X, LASER_ZOOM_X, LASER_ZOOM_X, LASER_ZOOM_X]
zoomY = [LASER_ZOOM_Y, LASER_ZOOM_Y, LASER_ZOOM_Y, LASER_ZOOM_Y]
sizeX = [LASER_SIZE_X, LASER_SIZE_X, LASER_SIZE_X, LASER_SIZE_X]
sizeY = [LASER_SIZE_Y, LASER_SIZE_Y, LASER_SIZE_Y, LASER_SIZE_Y]
finANGLE = [LASER_ANGLE, LASER_ANGLE, LASER_ANGLE, LASER_ANGLE]
swapX = [1,1,1,1]
swapY = [1,1,1,1]
warpdest = [[[-1500. ,1500.],[ 1500.,  1500.],[ 1500., -1500.],[-1500., -1500.]],
[[-1500. ,1500.],[ 1500.,  1500.],[ 1500., -1500.],[-1500., -1500.]],
[[-1500. ,1500.],[ 1500.,  1500.],[ 1500., -1500.],[-1500., -1500.]],
[[-1500. ,1500.],[ 1500.,  1500.],[ 1500., -1500.],[-1500., -1500.]]
]

# Etat global général
app_path = ""

# anciennement GameState
fs = GAME_FS_GAMEOVER
plyr = None
score = None


year = 2018
month = 8
day = 11