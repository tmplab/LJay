#!/bin/bash
#Modulateurs Accessible
#1 OSC1 (aka VCO1)
#2 OSC2 (aka VCO2)
#3 LFO1
#4 LFO2
#5 LFO3
#6 CV Generator
#7 ADSR
#8 Light Sensor
#9 Line IN (Audio IN jack)
#10 Midi (Keyboard ?) Velocity ?
#11 CV1 jack
#12 CV2 jack
#13 CV3 jack
#17 VCO1_OUT
#18 VCO2_OUT
#20 VCF_Out
#21 MIX_Out
#22 VCA_Out

if [[ -z $1 ]]
then
 CRV=0
else
 CRV=$1
fi

if [[ -z $2 ]]
then
 AXE="X"
else
 AXE=$2
fi

if [[ -z $3 ]]
then
 PORTN=8003
else
 PORTN=$3
fi

oscsend 127.0.0.1 $PORTN "/nozoid/$AXE" ii 0 $CRV #reset
oscsend 127.0.0.1 $PORTN "/nozoid/$AXE" ii 22 $CRV #VCA
./C.sh r $CRV $PORTN
