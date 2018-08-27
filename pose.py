#!/usr/bin/env python


import json

def getCOCO(d,posepoints):
    dots = []
    for dot in posepoints:
        if len(d['part_candidates'][0][str(dot)]) != 0:
        	dots.append((d['part_candidates'][0][str(dot)][0], d['part_candidates'][0][str(dot)][1]))
    return dots


def bodyCOCO(d):
	bodypoints = [10,9,8,1,11,12,13]
	return getCOCO(d,bodypoints)

def armCOCO(d):
	armpoints = [7,6,5,1,2,3,4]
	return getCOCO(d,armpoints)

def headCOCO(d):
	headpoints = [1,0]
	return getCOCO(d,headpoints)


#def Pose(fwork):
def Pose(frame):


	PL = 0
	dots = []
	posename ='poses/snap/COCOface/snap_00000000'+str("%04d"%frame)+'_keypoints.json'
	posefile = open(posename , 'r')
	print ""
	print frame
	posedatas = posefile.read()
	pose = json.loads(posedatas)
	#print pose
	print bodyCOCO(pose)
	print armCOCO(pose)
	print headCOCO(pose)
	


Pose(320)


'''
Pose
 COCO

cou 
1 0

yeux 
16 14 0 15 17

MPI
jambes
22 11 10 9 8 12 13 14 20 

bras 
7 6 5 1 2 3 4

cou tronc
8 1 0

yeux
18 16 0 15 17


main 
0 17 18 19 20
16 15 14 13 0
0 9 10 11 12
8 7 6 5 0
0 1 2 3 4

face 
bas 0 - 16
cils 26-22 21-17
OD 16 39
nez 27-30
OG 45 27
bouche 60-67 60
42 45

'''