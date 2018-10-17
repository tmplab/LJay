# coding=UTF-8

# from globalVars import * : seulement des pseudo-constantes
# Need huge clean up.
# Stays for backward compatibility

from math import pi
PI = pi

# Pretty old. Overriden by IPs in conf file now.
#etherIP="192.168.1.4"
etherIP="192.168.1.4"
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


LASER_CENTER_X = -6840
LASER_CENTER_Y = 5281
LASER_ZOOM_X = -41.7
LASER_ZOOM_Y = -38.8
LASER_SIZE_X = 32000
LASER_SIZE_Y = 32000
LASER_ANGLE = 0


NO_BGM = False
#NO_BGM = True




