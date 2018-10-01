#!/bin/bash
if [[ -z $1 ]]
then
 PORTN=8003
else
 PORTN=$1
fi
oscsend 127.0.0.1 $PORTN "/nozoid/X" ii 0 0
oscsend 127.0.0.1 $PORTN "/nozoid/X" ii 0 1
oscsend 127.0.0.1 $PORTN "/nozoid/X" ii 0 2
oscsend 127.0.0.1 $PORTN "/nozoid/X" ii 0 3
