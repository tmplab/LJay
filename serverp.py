'''
LJay v0.8

serverp.py

Multi process version for multiple lasers with pygame simulatore. 
Works with mainp.py
Need redis server launched :

redis-server -bind IPaddress.

Create one process per etherdream.
Each process access directly to redis :

- get point list to draw : /pl/lasernumber
- for report /lstt/lasernumber /lack/lasernumber /cap/lasernumber


'''
from __future__ import absolute_import
import time
from globalVars import *
import gstt
import redis
from multiprocessing import Process, Queue, TimeoutError 
import random, ast
import settings
settings.Read()
import newdacp
import homographyp
import argparse

gstt.debug = 2

print ""
print ""
print "LJay v0.8 Server."
print "Multilaser and redis style."
print "Launch one bridge process per etherdream."
print "Etherdream <-> redis keys like point lists, DAC status,..."
print ""
print "Help for command arguments : --help"
print "Arguments parsing if needed..."
argsparser = argparse.ArgumentParser(description="LJay Server. Multilaser and redis style. ")
argsparser.add_argument("-v","--verbose",help="Verbose level. May decrease rendering quality (0 by default)",type=int)
argsparser.add_argument("-l","--lasernumber",help="How many Etherdream are available (1-4, 4 by default)",type=int)
argsparser.add_argument("-r","--redisIP",help="Redis computer IP address (gstt.LjayServerIP by default)",type=str)

args = argsparser.parse_args()

if args.redisIP  != None:
    serverIP = args.redisIP
else:
    serverIP = gstt.LjayServerIP 

if args.verbose != None:
    debug = args.verbose
    gstt.debug = debug

if args.lasernumber != None:
    lasernumber = args.lasernumber -1

else: 
    lasernumber = 3

print "lasernumber :",lasernumber

def dac_process(number, pl):
    while True:
        try:
            d = newdacp.DAC(number,pl)
            d.play_stream()
        except Exception as e:

            import sys, traceback
            if gstt.debug == 2:
                print '\n---------------------'
                print 'Exception: %s' % e
                print '- - - - - - - - - - -'
                traceback.print_tb(sys.exc_info()[2])
                print "\n"
            pass

        except KeyboardInterrupt:
            sys.exit(0)
 


if __name__ == '__main__':

        
    print "redis used : ", serverIP
    r = redis.StrictRedis(host=serverIP , port=6379, db=0)
    print r

    '''
    for laserid in range(0,4):
        r.set('/lack/'+str(laserid),0)
        r.set('/lstt/'+str(laserid),0)
    '''
    
    # Some stupid lists for at launch.

    grid_points = [(300.0+random.randint(-100, 100), 200.0+random.randint(-100, 100), 0), (500.0+random.randint(-100, 100), 200.0+random.randint(-100, 100), 65280), (500.0+random.randint(-100, 100), 400.0+random.randint(-100, 100), 65280), (300.0+random.randint(-100, 100), 400.0+random.randint(-100, 100), 65280), (300.0+random.randint(-100, 100), 200.0+random.randint(-100, 100), 65280)]
    if r.set('/pl/0', str(grid_points)) == True:
        print "original /pl/0 ", ast.literal_eval(r.get('/pl/0'))

    grid_points = [(300.0+random.randint(-100, 100), 200.0+random.randint(-100, 100), 0), (500.0+random.randint(-100, 100), 200.0+random.randint(-100, 100), 65280), (500.0+random.randint(-100, 100), 400.0+random.randint(-100, 100), 65280), (300.0+random.randint(-100, 100), 400.0+random.randint(-100, 100), 65280), (300.0+random.randint(-100, 100), 200.0+random.randint(-100, 100), 65280)]
    if r.set('/pl/1', str(grid_points)) == True:
        print "original /pl/1 ", ast.literal_eval(r.get('/pl/1'))

    grid_points = [(300.0+random.randint(-100, 100), 200.0+random.randint(-100, 100), 0), (500.0+random.randint(-100, 100), 200.0+random.randint(-100, 100), 65280), (500.0+random.randint(-100, 100), 400.0+random.randint(-100, 100), 65280), (300.0+random.randint(-100, 100), 400.0+random.randint(-100, 100), 65280), (300.0+random.randint(-100, 100), 200.0+random.randint(-100, 100), 65280)]
    if r.set('/pl/2', str(grid_points)) == True:
        print "original /pl/2 ", ast.literal_eval(r.get('/pl/2'))

    grid_points = [(300.0+random.randint(-100, 100), 200.0+random.randint(-100, 100), 0), (500.0+random.randint(-100, 100), 200.0+random.randint(-100, 100), 65280), (500.0+random.randint(-100, 100), 400.0+random.randint(-100, 100), 65280), (300.0+random.randint(-100, 100), 400.0+random.randint(-100, 100), 65280), (300.0+random.randint(-100, 100), 200.0+random.randint(-100, 100), 65280)]
    if r.set('/pl/3', str(grid_points)) == True:
        print "original /pl/3 ", ast.literal_eval(r.get('/pl/3'))

    # Launch one process (a newdacp instance) by etherdream

    dac_worker0= Process(target=dac_process,args=(0,0))
    dac_worker0.start()
    
    if lasernumber >0:
        dac_worker1= Process(target=dac_process,args=(1,0))
        dac_worker1.start()

    if lasernumber >1:
        dac_worker2= Process(target=dac_process,args=(2,0))
        dac_worker2.start()
    
    if lasernumber >2:
        dac_worker3= Process(target=dac_process,args=(3,0))
        dac_worker3.start()

    # Main loop do nothing. Maybe do the webui server ?
    try:
        while True:
            time.sleep(0.1)
 
    except KeyboardInterrupt:
        pass

    # Gently stop on CTRL C

    finally:

        dac_worker0.join()
        if lasernumber >0:
            dac_worker1.join()
        if lasernumber >1:
            dac_worker2.join()
        if lasernumber >2:
            dac_worker3.join()
 
    
        for laserid in range(0,lasernumber+1):
            print "reset redis values for laser",laserid
            r.set('/lack/'+str(laserid),64)
            r.set('/lstt/'+str(laserid),64)
            r.set('/cap/'+str(laserid),0)
    
    print "Fin des haricots"