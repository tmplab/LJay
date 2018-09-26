#!/bin/bash
if [[ -z $1 ]]
then
 OSC=0
else
 OSC=$1
fi
if [[ -z $2 ]]
then
 PORTN=8003
else
 PORTN=$2
fi
oscsend 127.0.0.1 $PORTN "/nozoid/X" ii $OSC 0
oscsend 127.0.0.1 $PORTN "/nozoid/X" ii $OSC 1
oscsend 127.0.0.1 $PORTN "/nozoid/X" ii $OSC 2
oscsend 127.0.0.1 $PORTN "/nozoid/X" ii $OSC 3
oscsend 127.0.0.1 $PORTN "/nozoid/color" iiii 255 0 0 0
oscsend 127.0.0.1 $PORTN "/nozoid/color" iiii 255 0 255 1
oscsend 127.0.0.1 $PORTN "/nozoid/color" iiii 0 255 0 2
oscsend 127.0.0.1 $PORTN "/nozoid/color" iiii 0 0 255 3
