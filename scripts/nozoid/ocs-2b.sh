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

echo "./Y.sh 1 0 #OSC1"
./Y.sh 1 0 #OSC1
echo "./X.sh 2 0 #OSC2"
./X.sh 2 0 #OSC2
./C.sh r 0
echo "./Y.sh 2 2 #OSC2"
./Y.sh 2 2 #OSC2
echo "./X.sh 1 2 #OSC1"
./X.sh 1 2 #OSC1
./C.sh b 2

echo "./Y.sh 6 1 #CV Gen"
./Y.sh 6 1 #CV Gen
echo "./X.sh 7 1 #ADSR"
./X.sh 7 1 #ADSR
./C.sh g 1
echo "./Y.sh 7 3 #CV Gen"
./Y.sh 7 3 #CV Gen
echo "./X.sh 6 3 #ADSR"
./X.sh 6 3 #ADSR
./C.sh y 3
