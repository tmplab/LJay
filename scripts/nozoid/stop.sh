#!/bin/bash
if [[ -z $1 ]]
then
 PORTN=8003
else
 PORTN=$1
fi

oscsend 127.0.0.1 $PORTN "/nozoid/stop"
