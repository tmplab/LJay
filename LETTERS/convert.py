#!/usr/bin/python
import sys
import re

source = sys.argv[1]
content = file( source ).read()
L = []
L.append([";","\n"])
L.append(["^IN",""])
L.append(["PU.*",""])
L.append(["PD",""])

for pattern, replace in L :
    content = re.sub( pattern, replace, content)
parsed = re.split("\n", content)
tmp = []
out = []
MaxX = -9999999999999999
MaxY = -9999999999999999
MinX = 999999999999999
MinY = 999999999999999
first = None 
for line in parsed:
  if line == "" :
    continue
  tup = re.split(',',line)
  if len(tup) < 2 : continue
  x = int( ( int( tup[0] )) )
  y = int( ( int( tup[1] )) )
  MinX = x if x < MinX else MinX
  MaxX = x if x > MaxX else MaxX
  MinY = y if y < MinY else MinY
  MaxY = y if y > MaxY else MaxY
  tmp.append([x,y])
  if( first == None ):
      first = [x,y]
tmp.append( first )
moveX = ( MaxX + MinX ) / 2 
moveY = (  MaxY + MinY ) / 2 
for x,y in tmp:
    newX = x - moveX
    newY = y - moveY
    out.append( [ newX, newY ] )
print out

#if len(tmp) != 0:
#    out.append( tmp )

