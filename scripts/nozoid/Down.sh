#!/bin/bash
if [[ -z $1 ]]
then
 VAL=0
else
 VAL=$1
fi

if [[ -z $2 ]]
then
 PORTN=8003
else
 PORTN=$2
fi
oscsend 127.0.0.1 $PORTN "/nozoid/down" i $VAL
