import gstt
import argparse


def handle():

	print ""
	print "Arguments parsing if needed..."
	#have to be done before importing bhorosc.py to get correct port assignment
	argsparser = argparse.ArgumentParser(description="LJay")
	argsparser.add_argument("-i","--iport",help="OSC port number to listen to (8001 by default)",type=int)
	argsparser.add_argument("-o","--oport",help="OSC port number to send to (8002 by default)",type=int)
	argsparser.add_argument("-x","--invx",help="Invert X axis",action="store_true")
	argsparser.add_argument("-y","--invy",help="Invert Y axis",action="store_true")
	argsparser.add_argument("-s","--set",help="Specify wich generator set to use (default is in gstt.py)",type=int)
	argsparser.add_argument("-c","--curve",help="Specify with generator curve to use (default is in gstt.py)",type=int)
	argsparser.add_argument("-r","--reset",help="Reset alignement values",action="store_true")
	argsparser.add_argument("-l","--laser",help="Last digit of etherdream ip address 192.168.1.0/24 (4 by default). Localhost if digit provided is 0.",type=int)
	argsparser.add_argument("-d","--display",help="Point list number displayed in pygame simulator",type=int)
	argsparser.add_argument("-v","--verbose",help="Debug mode 0,1 or 2.",type=int)
	argsparser.add_argument("-L","--Lasers",help="Number of lasers connected.",type=int)

	args = argsparser.parse_args()


	# Ports arguments
	if args.iport:
		iport = args.iport
		gstt.iport = iport
	else:
		iport = gstt.iport

	if args.oport:
		oport = args.oport
		gstt.oport = oport
	else:
		oport = gstt.oport

	print "gstt.oport:",gstt.oport
	print "gstt.iport:",gstt.iport


	# X Y inversion arguments
	if args.invx == True:

		gstt.swapx = -1 * gstt.swapx
		gstt.centerx = 0
		gstt.centery = 0
		#WriteSettings()
		print("X invertion Asked")
		if gstt.swapx == 1:
			print ("X not Inverted")
		else:
			print ("X Inverted")

	if args.invy == True:

		gstt.swapy = -1 * gstt.swapy
		gstt.centerx = 0
		gstt.centery = 0
		#WriteSettings()
		print("Y invertion Asked")
		if gstt.swapy == 1:
			print ("Y not Inverted")
		else:
			print("Y inverted")



	# Set / Curves arguments
	if args.set != None:
		gstt.Set = args.set
		print "Set : " + str(gstt.Set)

	if args.curve != None:
		gstt.Curve = args.curve
		print "Curve : " + str(gstt.Curve)


	# Point list number used by simulator
	if args.display  != None:
		gstt.simuPL = args.display



	# Verbose = debug
	if args.verbose  != None:
		gstt.debug = args.verbose
	

	# Lasers = number of laser connected
	if args.Lasers  != None:
		gstt.LaserNumber = args.Lasers
	
	
	# Etherdream target
	if args.laser  != None:
		lstdgtlaser = args.laser
		if lstdgtlaser == 0:
			etherIP = "127.0.0.1"
		else:
			etherIP = "192.168.1."+str(lstdgtlaser)

	else:
		etherIP = "192.168.1.4"

	print ("Laser 1 etherIP:",etherIP)

	# Reset alignment values
	if args.reset == True:

		gstt.centerx = 0
		gstt.centery = 0
		gstt.zoomx = 15
		gstt.zoomy = 15
		gstt.sizex = 32000
		gstt.sizey = 32000
		gstt.finangle = 0.0
		gstt.swapx = 1
		gstt.swapy = 1
		#WriteSettings()
	