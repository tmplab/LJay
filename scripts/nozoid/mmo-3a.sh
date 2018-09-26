#!/bin/bash
oscsend 127.0.0.1 8003 "/nozoid/Y" ii 4 0 #LFO1
oscsend 127.0.0.1 8003 "/nozoid/Y" ii 5 1 #LFO2
oscsend 127.0.0.1 8003 "/nozoid/Y" ii 6 2 #LFO3
oscsend 127.0.0.1 8003 "/nozoid/Y" ii 7 3 #ADSR
oscsend 127.0.0.1 8003 "/nozoid/X" ii 9 0 #Line IN
oscsend 127.0.0.1 8003 "/nozoid/X" ii 9 1
oscsend 127.0.0.1 8003 "/nozoid/X" ii 9 2
oscsend 127.0.0.1 8003 "/nozoid/X" ii 9 3
oscsend 127.0.0.1 8003 "/nozoid/color" iiii 255 0 0 0
oscsend 127.0.0.1 8003 "/nozoid/color" iiii 255 0 255 1
oscsend 127.0.0.1 8003 "/nozoid/color" iiii 0 255 0 2
oscsend 127.0.0.1 8003 "/nozoid/color" iiii 0 0 255 3
