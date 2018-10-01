#!/bin/bash
if [[ -z $1 ]]
then
 OSC=1
else
 OSC=$1
fi
if [[ -z $2 ]]
then
 CRV=0
else
 CRV=$2
fi
if [[ -z $3 ]]
then
 AXE="Y"
else
 AXE=$3
fi
if [[ -z $4 ]]
then
 PORTN=8005
else
 PORTN=$4
fi
oscsend 127.0.0.1 $PORTN "/nozoid/$AXE" ii $OSC $CRV

