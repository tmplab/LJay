#!/usr/bin/env python


import json
import gstt, os

shift = [400,200]

# get absolute body position points
def getCOCO(d,posepoints):
    dots = []
    for dot in posepoints:
        if len(d['part_candidates'][0][str(dot)]) != 0:
        	print d['part_candidates'][0][str(dot)]
        	print dot
        	#print len(d['part_candidates'][0][str(dot)])  
        	if len(d['part_candidates'][0][str(dot)]) > 3 and 0 < dot < posepoints:
        		print str(dot-1), str(dot), str(dot+1)
        		print d['part_candidates'][0][str(dot)][0], d['part_candidates'][0][str(dot)][3], d['part_candidates'][0][str(dot-1)][0] , d['part_candidates'][0][str(dot)][0], d['part_candidates'][0][str(dot+1)][0]  
        		if (d['part_candidates'][0][str(dot-1)][0] < d['part_candidates'][0][str(dot)][0] < d['part_candidates'][0][str(dot+1)][0]) or (d['part_candidates'][0][str(dot-1)][0] > d['part_candidates'][0][str(dot)][0] > d['part_candidates'][0][str(dot+1)][0]):
        			print d['part_candidates'][0][str(dot)][0]
        		else: 
        			print d['part_candidates'][0][str(dot)][3]
        	dots.append((d['part_candidates'][0][str(dot)][0], d['part_candidates'][0][str(dot)][1]))
    return dots

# get relative (-1 1) face position points
def getBODY(d,posepoints):

	dots = []
	for dot in posepoints:

		if len(d['people'][0]['pose_keypoints_2d']) != 0:
			print dot, d['people'][0]['pose_keypoints_2d'][dot * 3], d['people'][0]['pose_keypoints_2d'][(dot * 3)+1]
			#dots.append((d['people'][0]['pose_keypoints_2d'][dot * 3], d['people'][0]['pose_keypoints_2d'][(dot * 3)+1]))
	return dots


# get absolute face position points
def getFACE(d,posepoints):

	dots = []
	for dot in posepoints:

		if len(d['people'][0]['face_keypoints']) != 0:
			#print dot, d['people'][0]['face_keypoints'][dot * 3], d['people'][0]['face_keypoints'][(dot * 3)+1]
			dots.append((d['people'][0]['face_keypoints'][dot * 3], d['people'][0]['face_keypoints'][(dot * 3)+1]))
	return dots


# body parts
def bodyCOCO(d):
	bodypoints = [10,9,8,1,11,12,13]
	#return getCOCO(d,bodypoints)
	return getBODY(d,bodypoints)

def armCOCO(d):
	armpoints = [7,6,5,1,2,3,4]
	return getCOCO(d,armpoints)

def headCOCO(d):
	headpoints = [1,0]
	return getCOCO(d,headpoints)

def checkDOTS(dots):
	print dots



# Face keypoints
def faceCOCO(d):
    posepoints = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
    return getFACE(d,posepoints)


def browL(d):
    posepoints = [26,25,24,23,22]
    return getFACE(d,posepoints)

def browR(d):
    posepoints = [21,20,19,18,17]
    return getFACE(d,posepoints)

def eyeR(d):
    posepoints = [36,37,38,39,40,41,36]
    return getFACE(d,posepoints)


def eyeL(d):
    posepoints = [42,43,44,45,46,47,42]
    return getFACE(d,posepoints)

def nose(d):
    posepoints = [27,28,29,30]
    return getFACE(d,posepoints)

def mouth(d):
    posepoints = [48,59,58,57,56,55,54,53,52,51,50,49,48,60,67,66,65,64,63,62,61,60]
    return getFACE(d,posepoints)


#def Pose(fwork):
def Pose(pose_dir):

	print "Check directory ",'poses/' + pose_dir + '/'
	numfiles = sum(1 for f in os.listdir('poses/' + pose_dir + '/') if os.path.isfile(os.path.join('poses/' + pose_dir + '/', f)) and f[0] != '.')
	print "Pose : ", pose_dir, numfiles, "images"

	for frame in xrange(numfiles):

		#posename = pose_dir + 'snap_00000000'+str("%04d"%frame)+'_keypoints.json'
		posename = 'poses/' + pose_dir + '/' + pose_dir +'-'+str("%05d"%frame)+'.json'
		posefile = open(posename , 'r')
		print ""
		print "frame ",frame
		posedatas = posefile.read()
		pose = json.loads(posedatas)
		#print pose
		print ""
		#print pose
		'''
		if len(pose['people'][0]['face_keypoints']) != 0:
			print len(pose['people'])
			for facepoint in xrange(61):
				print facepoint, pose['people'][0]['face_keypoints'][facepoint * 3], pose['people'][0]['face_keypoints'][(facepoint * 3)+1]
				'''
		#print eyeR(pose)
		dots = bodyCOCO(pose)
		print dots
		#dots = armCOCO(pose)
		#dots = headCOCO(pose)
			


Pose('window1')


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