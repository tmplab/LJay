#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# -*- mode: Python -*-
'''
ws:
{
    "velocity" : 0.5,
    "expressivity" : 0.5,
    "sensibility"  : 0.5,
    "beauty": 0.5
}

'''
from globalVars import *
import colorify
import json
import gstt
import math
import random
from os import path

# https://pypi.org/project/opensimplex/
from opensimplex import OpenSimplex


class Agent :
    settings = {
        'max_acceleration' : 50,
        'max_points' : 30,
        'max_speed' : PI * 0.125,
        'max_velocity' : 0,
        'mean_radius' : 400,
        'max_radius' : 800,
        'friction_coefficient' : 0,
    }
    composition = {
        "rotation_speed"              : 10,
        "points_cardinality"          : 10,
        "default_radius"              : 10,
        "radius_variation"            : 10,
        "velocity_variation"          : 10,
        "symmetry_probability"        : 10
    }
    state = {
        'counter' : 0,
        'current_point_velocity' : 0,
        'current_radius' : 0,
        'current_acceleration' : 0,
        'rotation_angle' : 0,
        'terminal_velocity' : 0,
        'size' : 36,
    }
    worldstate = {}
    noiseTable = []
    pointsList = {}
    clock = 0

    def __init__(self):
        self.start()
        # Open DB connection
        # Open API connection
        # Open Debugger port

    def status(self):
          # Check DB
          # check API
          # check lazer
        pass


    def start(self, settings =  {}):

        if not(path.isfile( '/tmp/ws.json')):
            handle = open( '/tmp/ws.json','w')
            handle.write('{"velocity" : 0.50,"expressivity" : 0.0,"sensibility"  : 0.15,"beauty": 0.1}');
            handle.close();

        self.settings.update( settings )
        state = self.state
        sett = self.settings
        self.worldstate = {}
        self.worldstate['current'] = {}

        # pointsList needs to be bootstraped
        bootstrapList = list( {'angle':0,'velocity':0,'coordinates':[0,0],'radius':10} for i in range(self.settings['max_points']) )
        self.pointsList = {-1 : bootstrapList, 0 : bootstrapList}
        
        # Generate new random source
        seed = int( random.random() * 1024 )
        noise = OpenSimplex(seed= seed )
        octaves = 3
        freq = 16.0 * octaves

        for x in range(sett['max_points']):
            tmp = []
            for y in range(sett['max_points']):
                n = noise.noise2d( x=x, y=y )
                tmp.append ( n ) 
            self.noiseTable.append(tmp) 

    def getWorldstate(self):
        with open( "/tmp/ws.json","r") as file :
            content = file.read()
            current = json.loads(content)
            self.worldstate["old"] = self.worldstate["current"]
            self.worldstate["current"] = current
        return current

    def storeWorldState(self):
        pass

    def storeComposition(self):
        pass

    def run(self):

        # Get worldstate(n)
        
        comp = self.composition
        world = self.getWorldstate()
        sett = self.settings
        stat = self.state

        # Compare to worldstate(n-1)
        if( self.worldstate["old"] != world ):

            comp['default_radius']              = sett['mean_radius'] * world['velocity']

            amp = sett['max_radius'] - sett['mean_radius'] 
            comp['radius_variation']            = amp * world['expressivity']

            comp['rotation_speed']              = sett['max_speed'] * world['sensibility']

            n = int( sett['max_points'] * world['beauty'] ) 
            comp['points_cardinality']          = n if n > 2 else 3

            # Caution, this is an in/out force, not a radial / centripetal one
            comp['velocity_variation']          = sett['max_acceleration'] * world['sensibility']

            comp['symmetry_probability']        = world['beauty'] 

            # Store worldstate(n)
            self.storeWorldState()

            # Store composition(n)
            self.storeComposition()

        self.setNewState()  

        stat['counter'] +=  1
        return self.getPoints()

    def getSymmetricPoint(self, Nth):
        """
        Returns symetric point relative to self
        f(Nth,sp,pc)                         = Nth % (pc / (pc*sp + 1) )
        pc=10
        ___________________________sp________________________________
        |N   |  0   0,1  0,2  0,3  0,4  0,5  0,6  0,7  0,8  0,9   1 |
        |___________________________________________________________|
        |0   |  0    0    0    0    0    0    0    0    0    0    0 |
        |1   |  1    1    1    1    1    1    1    1    1    0    0 |
        |2   |  2    2    2    2    0    0    0    0    0    0    0 |
        |3   |  3    3    3    0    1    1    0    0    0    0    0 |
        |4   |  4    4    0    1    0    0    1    0    0    0    0 |
        |5   |  5    0    1    0    1    0    0    0    0    0    0 |
        |6   |  6    1    2    1    0    1    0    1    0    0    0 |
        |7   |  7    2    0    2    1    0    1    0    0    0    0 |
        |8   |  8    3    1    0    0    1    0    0    0    0    0 |
        |9   |  9    4    2    1    1    0    0    0    0    0    0 |
        |___________________________________________________________|
        |axis|  1    2    3    4    5    6    7    8    9    10   11|
        |___________________________________________________________|
        """
        symmetry_probability = self.composition['symmetry_probability']
        points_cardinality   = self.composition['points_cardinality']
        axis                         = math.floor(points_cardinality * symmetry_probability) + 1
        return int(math.floor(math.fmod(Nth,points_cardinality/axis)))
    
    def setNewState( self ):

        comp = self.composition
        stat = self.state

        stat['min_radius']                                  = comp['default_radius'] - comp['radius_variation']
        if( stat['min_radius'] < 0 ):
            stat['min_radius']                              = 0

        if( stat['current_radius'] < stat['min_radius'] ):
            stat['current_radius']                    = stat['min_radius']
        stat['current_radius']                    = comp['default_radius']

        stat['max_radius']                                  = comp['default_radius'] + comp['radius_variation']
        if( stat['current_radius'] > stat['max_radius'] ):
            stat['current_radius']                    = stat['max_radius']

#        stat['rotation_angle'] += 2 * PI / math.pow( comp['points_cardinality'],2)
        stat['rotation_angle'] += comp['rotation_speed']
        if( stat['rotation_angle'] > 2 * PI ):
            stat['rotation_angle']= stat['rotation_angle'] % ( 2 * PI)
        stat['current_acceleration']                             = comp['velocity_variation'] if stat['current_point_velocity'] > 0 else  -comp['velocity_variation']

    def getPointDynamic(self, point) :
        '''
        Returns current_radius, velocity given point[angle, velocity] and global[angular_speed,default_radius,radius_variation,velocity_variation]
        '''
        comp = self.composition
        stat = self.state
        sett = self.settings
        positive = true if point['velocity'] > 0 else false 

        absolute_velocity                           = ( point['velocity'] * sett['friction_coefficient'] ) + stat['current_acceleration']
        if( absolute_velocity > sett['max_velocity'] ):
            absolute_velocity                       = sett['max_velocity']
        terminal_velocity      = absolute_velocity if positive else (- absolute_velocity)
        energy                                      = absolute_velocity
        terminal_radius                                      = point['radius'] 
        # while there is energy
        while ( energy > 0 ):
            my_radius                                 = point['radius'] + energy

        """        
        # while there is energy
        while ( math.fabs(energy) > 0 ):
            my_radius                                 = point['radius'] + energy

            # get new radius = radius + velocity
            print( 'energy', energy)
            # if energy drives point out of bound, clip and reduce enery
            if( my_radius > sett['max_radius'] ) :
              # 40 - 35 - 80 = -75
              energy                                  = ( stat['max_radius'] - stat['current_radius']) - ( energy * sett['friction_coefficient'] )
              my_radius                               = stat['max_radius']
            else :
              # - ( 35 - 20 ) - ( -80 ) = 65
              my_radius                               = stat['min_radius']
            
            current_radius                            = my_radius
        
        """
        return [terminal_radius, terminal_velocity]

    def getPoints(self):
        comp = self.composition
        stat = self.state
        sett = self.settings

        for i in range( comp['points_cardinality'] ):
            self.pointsList[0][i]['angle']               = self.pointsList[-1][i]['angle'] + 2 * PI * i / comp['points_cardinality'] + stat['rotation_angle']
            tmp_radius                           = self.pointsList[-1][i]['radius']
            ref = self.getSymmetricPoint(i)
            if (ref != i ):
                print "ref",ref
                tmp_velocity                    = self.pointsList[0][ref]['velocity']
            else:
                velocity,radius                 = self.getPointDynamic( self.pointsList[-1][i])
                pointsList[n][i]['velocity']    = velocity
                pointsList[n][i]['radius']      = radius
                pointsList[n][i]['coordinates'] = getPointCoordinates( self.pointsList[-1][i] )


        self.pointsList[-1] = self.pointsList[0]
        return self.pointsList

        dots = []
        current_radius = stat['current_radius']
        radius_variation= comp['radius_variation']
        points_cardinality = len( self.noiseTable ) - 1 
        n = stat['counter'] % len(self.noiseTable)
        for point in range(0, comp['points_cardinality'] +1 ) :
            x = (current_radius+radius_variation*( self.noiseTable[n][point]  )+0.5)*math.cos(2 * PI  * point /  float(comp['points_cardinality']) + stat['rotation_angle'] )
            y = ( current_radius+radius_variation*( self.noiseTable[n][point] )+0.5)*math.sin(2 * PI * point / float(comp['points_cardinality']) + stat['rotation_angle'] )
            dots.append([int(x),int(y)])
        
        return dots        


agent = Agent()


# Mode 0
def Circle(fwork):
    pointsList = agent.run()
    projected = []
    for dots in pointsList : 
        projected.append( proj(int(dots[0]),int(dots[1]),0 ) )
    fwork.PolyLineOneColor( projected, c=colorify.rgb2hex(gstt.color)  )

# Why the heck do we need that ?

def cc2range(s,min,max):
    a1, a2 = 0,127  
    b1, b2 = min, max
    return  b1 + ((s - a1) * (b2 - b1) / (a2 - a1))


def proj(x,y,z):

    gstt.angleX += cc2range(gstt.cc[29],0,0.1)
    gstt.angleY += cc2range(gstt.cc[30],0,0.1)
    gstt.angleZ += cc2range(gstt.cc[31],0,0.1)
    
    rad = gstt.angleX * PI / 180
    cosa = math.cos(rad)
    sina = math.sin(rad)
    y2 = y
    y = y2 * cosa - z * sina
    z = y2 * sina + z * cosa

    rad = gstt.angleY * PI / 180
    cosa = math.cos(rad)
    sina = math.sin(rad)
    z2 = z
    z = z2 * cosa - x * sina
    x = z2 * sina + x * cosa

    rad = gstt.angleZ * PI / 180
    cosa = math.cos(rad)
    sina = math.sin(rad)
    x2 = x
    x = x2 * cosa - y * sina
    y = x2 * sina + y * cosa

    # 3D to 2D projection
    factor = 4 * gstt.cc[22] / ((gstt.cc[21] * 8) + z)
    x = x * factor + xy_center [0]
    y = - y * factor + xy_center [1]

    return x,y

