# coding=UTF-8

# from globalVars import * : seulement des pseudo-constantes
from math import pi
PI = pi

# If you don't have an ether dream connected use localhost.
# etherIP="localhost"

# Enter here your ether dream IP
#etherIP="192.168.1.4"
etherIP="192.168.1.3"
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


'''
LASER_CENTER_X = 2360
LASER_CENTER_Y = 12901
LASER_ZOOM_X = -35.5
LASER_ZOOM_Y = - 33.2
LASER_SIZE_X = 25000
LASER_SIZE_Y = 25000
LASER_ANGLE = 0

#-16040,11781,-26.2,-20.6,25000,25000
#etherIP="192.168.1.6"
'''
LASER_CENTER_X = -6840
LASER_CENTER_Y = 5281
LASER_ZOOM_X = -41.7
LASER_ZOOM_Y = -38.8
LASER_SIZE_X = 32000
LASER_SIZE_Y = 32000
LASER_ANGLE = 0
'''

LASER_CENTER_X = -16000
LASER_CENTER_Y = 11780
LASER_ZOOM_X = -26
LASER_ZOOM_Y = -20
LASER_SIZE_X = 25000
LASER_SIZE_Y = 25000
LASER_ANGLE = 0

LASER_CENTER_X = 0
LASER_CENTER_Y = 1
LASER_ZOOM_X = -56
LASER_ZOOM_Y = -71
LASER_SIZE_X = 25000
LASER_SIZE_Y = 25000
LASER_ANGLE = 0

LASER_CENTER_X = 5400
LASER_CENTER_Y = -9000
LASER_ZOOM_X = 23
LASER_ZOOM_Y = 40
LASER_SIZE_X = 25000
LASER_SIZE_Y = 25000

ER_ANGLE = 0
'''

NO_BGM = False
#NO_BGM = True




