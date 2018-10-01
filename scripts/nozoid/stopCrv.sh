#!/bin/bash
if [[ -z $1 ]]
then
 CRV=0
else
 CRV=$1
fi
if [[ -z $2 ]]
then
 PORTN=8003
else
 PORTN=$2
fi
oscsend 127.0.0.1 $PORTN "/nozoid/X" ii 0 $CRV
oscsend 127.0.0.1 $PORTN "/nozoid/Y" ii 0 $CRV
