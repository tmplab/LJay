#!/bin/bash
if [[ -z $1 ]]
then
 CRV=0
else
 CRV=$1
fi
oscsend 127.0.0.1 8003 "/nozoid/X" ii 0 $CRV
oscsend 127.0.0.1 8003 "/nozoid/Y" ii 0 $CRV
