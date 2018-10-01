#!/bin/bash
oscsend 127.0.0.1 8005 "/nozoid/X" ii 1 0 #OSC1
oscsend 127.0.0.1 8005 "/nozoid/Y" ii 7 0 #ADSR

oscsend 127.0.0.1 8005 "/nozoid/X" ii 7 2 #ADSR
oscsend 127.0.0.1 8005 "/nozoid/Y" ii 2 2 #OSC2

oscsend 127.0.0.1 8005 "/nozoid/X" ii 0 1 #None
oscsend 127.0.0.1 8005 "/nozoid/Y" ii 0 1 #None

oscsend 127.0.0.1 8005 "/nozoid/X" ii 0 3 #None
oscsend 127.0.0.1 8005 "/nozoid/Y" ii 0 3 #None

oscsend 127.0.0.1 8005 "/nozoid/color" iiii 0 0 255 0
oscsend 127.0.0.1 8005 "/nozoid/color" iiii 0 255 0 2
