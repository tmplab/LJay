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

oscsend 127.0.0.1 8005 "/nozoid/Y" ii 4 0 #LFO1
oscsend 127.0.0.1 8005 "/nozoid/Y" ii 5 1 #LFO2
oscsend 127.0.0.1 8005 "/nozoid/Y" ii 7 2 #ADSR
oscsend 127.0.0.1 8005 "/nozoid/Y" ii 9 3 #Line IN
oscsend 127.0.0.1 8005 "/nozoid/X" ii 6 0 #LFO3
oscsend 127.0.0.1 8005 "/nozoid/X" ii 6 1
oscsend 127.0.0.1 8005 "/nozoid/X" ii 6 2
oscsend 127.0.0.1 8005 "/nozoid/X" ii 6 3
oscsend 127.0.0.1 8005 "/nozoid/color" iiii 255 0 0 0
oscsend 127.0.0.1 8005 "/nozoid/color" iiii 255 0 255 1
oscsend 127.0.0.1 8005 "/nozoid/color" iiii 0 255 0 2
oscsend 127.0.0.1 8005 "/nozoid/color" iiii 0 0 255 3
