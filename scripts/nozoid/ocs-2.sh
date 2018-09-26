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

oscsend 127.0.0.1 8003 "/nozoid/Y" ii 3 0 #LFO1
oscsend 127.0.0.1 8003 "/nozoid/Y" ii 20 1 #VCF
oscsend 127.0.0.1 8003 "/nozoid/Y" ii 5 2 #LFO3
oscsend 127.0.0.1 8003 "/nozoid/Y" ii 7 3 #ADSR
oscsend 127.0.0.1 8003 "/nozoid/X" ii 4 0 #LFO2
oscsend 127.0.0.1 8003 "/nozoid/X" ii 4 1
oscsend 127.0.0.1 8003 "/nozoid/X" ii 4 2
oscsend 127.0.0.1 8003 "/nozoid/X" ii 4 3
oscsend 127.0.0.1 8003 "/nozoid/color" iiii 255 0 0 0
oscsend 127.0.0.1 8003 "/nozoid/color" iiii 255 0 255 1
oscsend 127.0.0.1 8003 "/nozoid/color" iiii 0 255 0 2
oscsend 127.0.0.1 8003 "/nozoid/color" iiii 0 0 255 3
