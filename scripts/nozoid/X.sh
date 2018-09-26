#!/bin/bash
if [[ -z $1 ]]
then
 oscsend 127.0.0.1 8003 "/nozoid/X" 
 oscsend 127.0.0.1 8005 "/nozoid/X" 
else
 OSC=$1
 if [[ -z $2 ]]
 then
  CRV=0
 else
  CRV=$2
 fi
 if [[ -z $3 ]]
 then
  PORTN=8003
 else
  PORTN=$3
 fi
 oscsend 127.0.0.1 $PORTN "/nozoid/X" ii $OSC $CRV
fi

