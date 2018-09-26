#!/bin/bash
if [[ -z $1 ]]
then
 CLR="w"
else
 CLR=$1
fi

#echo $CLR

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


if [[ "w" == $CLR ]]
then
 CLR="255 255 255"
fi

if [[ "r" == $CLR ]]
then
 CLR="255 0 0"
fi

if [[ "g" == $CLR ]]
then
 CLR="0 255 0"
fi

if [[ "b" == $CLR ]]
then
 CLR="0 0 255"
fi

if [[ "y" == $CLR ]]
then
 CLR="255 255 0"
fi

if [[ "c" == $CLR ]]
then
 CLR="0 255 255"
fi

if [[ "m" == $CLR ]]
then
 CLR="255 0 255"
fi

#echo $CLR

oscsend 127.0.0.1 $PORTN "/nozoid/color" iiii $CLR $CRV
