#!/bin/bash
#Modulateurs Accessible
#1 OSC1 (aka VCO1)
#2 OSC2 (aka VCO2)
#3 OSC3 (aka VCO3)
#4 LFO1
#5 LFO2
#6 LFO3
#7 ADSR
#8 CV Ext
#9 Line IN
#10 Joystick
#11 Audio_In Left
#12 Audio_In Right
#13 Automodulation ?
#17 VCO1_OUT
#18 VCO2_OUT
#19 VCO3_OUT
#20 Audio_Out Right
#21 Audio_Out Left

if [[ -z $1 ]]
then
 CRV=0
else
 CRV=$1
fi

if [[ -z $2 ]]
then
 AXE="Y"
else
 AXE=$2
fi


if [[ -z $3 ]]
then
 PORTN=8005
else
 PORTN=$3
fi

oscsend 127.0.0.1 $PORTN "/nozoid/$AXE" ii 0 $CRV #reset
oscsend 127.0.0.1 $PORTN "/nozoid/$AXE" ii 2 $CRV #OSC2
