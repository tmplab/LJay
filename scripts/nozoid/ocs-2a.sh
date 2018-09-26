#!/bin/bash
oscsend 127.0.0.1 8003 "/nozoid/X" ii 4 0 #LFO3
oscsend 127.0.0.1 8003 "/nozoid/Y" ii 7 0 #ADSR

oscsend 127.0.0.1 8003 "/nozoid/X" ii 3 2 #LFO1
oscsend 127.0.0.1 8003 "/nozoid/Y" ii 20 2 #VCF

oscsend 127.0.0.1 8003 "/nozoid/X" ii 0 1 #None
oscsend 127.0.0.1 8003 "/nozoid/Y" ii 0 1 #None
oscsend 127.0.0.1 8003 "/nozoid/X" ii 0 3 #None
oscsend 127.0.0.1 8003 "/nozoid/Y" ii 0 3 #None

oscsend 127.0.0.1 8003 "/nozoid/color" iiii 255 0 0 0
oscsend 127.0.0.1 8003 "/nozoid/color" iiii 0 255 0 2
