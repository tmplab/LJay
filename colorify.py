#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# -*- mode: Python -*-

import gstt


def hex2rgb(hexcode):
    return tuple(map(ord,hexcode[1:].decode('hex')))


def rgb2hex(rgb):
    return int('0x%02x%02x%02x' % tuple(rgb),0)



def red(state):

    if state == 1: 
        gstt.color[0] = 255
    if state == 0: 
        gstt.color[0] = 0
        
 
def blue(state):

    if state == 1: 
        gstt.color[1] = 255
    if state == 0: 
        gstt.color[1] = 0
        
def green(state):

    if state == 1: 
        gstt.color[2] = 255
    if state == 0: 
        gstt.color[2] = 0
 
 
def interactive():

    pass             
        
def rainbow():

        gstt.color = list(((rgb2hex(gstt.color)+(gstt.cc[4]*5)) >> Val) & 255 for Val in (16, 8, 0))
        '''
        if gstt.color[0] > 254:
            gstt.color[1] += 1     
                   
            if gstt.color[1] > 254:
                gstt.color[2] += 1
                
            else:
                gstt.color[1] += 1          
        else:
            gstt.color[0] += 1
        
        if gstt.color[0] > 254 and gstt.color[1] > 2544  and gstt.color[2] > 254 :
            
            gstt.color[0] = 0
            gstt.color[1] = 0
            gstt.color[2] = 0
        '''    

jumptable =  {
        0: interactive,
        1: rainbow    }
    
def jump():

    doit = jumptable.get(gstt.colormode)
    doit()
    
    '''
    if gstt.colormode ==1:
        red()
        
    if gstt.colormode ==2:
        rainbow()    
    '''