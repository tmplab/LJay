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

./Y.sh 1 0 #OSC1
./C.sh r 0
./Y.sh 5 1 #LFO3
./C.sh g 1
./Y.sh 20 2 #VCF
./C.sh b 2
./Y.sh 7 3 #ADSR
./C.sh w 3
