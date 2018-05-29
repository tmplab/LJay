# coding=UTF-8

# from globalVars import * : seulement des pseudo-constantes
from math import pi


# If you don't have an ether dream connected use localhost.
# etherIP="localhost"

# Enter here your ether dream IP
#Laser Jaune (Rouge Vert)
#etherIP="192.168.1.4"
#config à droite
#5740,-11739,-36.1,-32.3,25000,25000
#LASER_CENTER_X = 5740
#LASER_CENTER_Y = -11739
#LASER_ZOOM_X = -36.1
#LASER_ZOOM_Y = -32.3
#LASER_SIZE_X = 25000
#LASER_SIZE_Y = 25000
#config un peu plus à gauche
#7580,-10979,-33.3,-31.9,25000,25000
#LASER_CENTER_X = 7580
#LASER_CENTER_Y = -10979
#LASER_ZOOM_X = -33.3
#LASER_ZOOM_Y = -31.9
#LASER_SIZE_X = 25000
#LASER_SIZE_Y = 25000

#Laser Blanc (Rouge Vert Bleu)
#Scene Haute
#1360,-13719,-48.2,-36.9,25000,25000
etherIP="192.168.1.5"
LASER_CENTER_X = 1360
LASER_CENTER_Y = -13719
LASER_ZOOM_X = -48.2
LASER_ZOOM_Y = -36.9
LASER_SIZE_X = 25000
LASER_SIZE_Y = 25000

#Laser Jaune (Rouge Vert)
#-6840,5281,-41.7,-38.8,25000,25000
#etherIP="192.168.1.6"
#LASER_CENTER_X = -6840
#LASER_CENTER_Y = 5281
#LASER_ZOOM_X = -41.7
#LASER_ZOOM_Y = -38.8
#LASER_SIZE_X = 25000
#LASER_SIZE_Y = 25000


#etherIP="192.168.1.1"
#etherIP="localhost"


# screen_size = [850,600]
screen_size = [800,600]
# screen_size = [100,100]
space = 200
strings = 9
COLOR_ON =  0xFFFFFF
COLOR_OFF =  0x000000
STRING_SIZE = 40
colorshex = [0xFF0000, 0xFF0000, 0xFF0000, 0xFF0000, 0xFF0000, 0xFF0000, 0xFF0000, 0xFF0000, 0xFF0000, 0xFF0000]

xy_center = [screen_size[0]/2,screen_size[1]/2]

harp_pos = [0,200]
DEFAULT_SPOKES = range(0,359,60)
DEFAULT_PLAYER_EXPLODE_COLOR = 0xFF0000
DEFAULT_SIDE_COUNT = 6
DREARRANGE_SIDES = .02

CRASH_SHAKE_MAX = 6
TDN_CRASH = 200

GAME_FS_QUIT = -1
GAME_FS_MENU = 0
GAME_FS_PLAY = 1
GAME_FS_GAMEOVER = 2

#LASER_CENTER_X = 0
#LASER_CENTER_Y = 1
#LASER_ZOOM_X = -56
#LASER_ZOOM_Y = -71
#LASER_SIZE_X = 25000
#LASER_SIZE_Y = 25000
# LASER_SIZE_X = 25000
# LASER_SIZE_Y = 25000
LASER_ANGLE = 0

NO_BGM = False
#NO_BGM = True

PI = pi


