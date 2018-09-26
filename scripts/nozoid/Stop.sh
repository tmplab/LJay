#!/bin/bash
if [[ -z $1 ]]
then
 PORTN=8003
else
 PORTN=$1
fi

./stopX.sh 0 $PORTN
./stopY.sh 0 $PORTN
