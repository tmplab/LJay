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

./X.sh 20 0 #VCF
./Y.sh 1 0 #OSC1
./C.sh r 0
./X.sh 1 2
./Y.sh 20 2
./C.sh b 2

./X.sh 20 1 #VCF
./Y.sh 2 1 #OSC2
./C.sh g 1
./X.sh 2 3
./Y.sh 20 3
./C.sh y 3
