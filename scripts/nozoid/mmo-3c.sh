#!/bin/bash
oscsend 127.0.0.1 8003 "/nozoid/X" ii 6 0 #LFO3 on curvenumber 0 (lissajous)
oscsend 127.0.0.1 8003 "/nozoid/Y" ii 7 0 #ADSR on curvenumber 0

oscsend 127.0.0.1 8003 "/nozoid/X" ii 7 2 #ADSR
oscsend 127.0.0.1 8003 "/nozoid/Y" ii 6 2 #LFO3

oscsend 127.0.0.1 8003 "/nozoid/X" ii 6 1 #LFO3
oscsend 127.0.0.1 8003 "/nozoid/Y" ii 4 1 #LFO1

oscsend 127.0.0.1 8003 "/nozoid/X" ii 4 3 #LFO1
oscsend 127.0.0.1 8003 "/nozoid/Y" ii 6 3 #LFO3

oscsend 127.0.0.1 8003 "/nozoid/color" iiii 0 0 255 0
oscsend 127.0.0.1 8003 "/nozoid/color" iiii 255 0 0 2
oscsend 127.0.0.1 8003 "/nozoid/color" iiii 0 255 0 1
oscsend 127.0.0.1 8003 "/nozoid/color" iiii 255 255 0 3
