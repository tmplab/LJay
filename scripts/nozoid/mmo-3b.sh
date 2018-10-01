#!/bin/bash
oscsend 127.0.0.1 8005 "/nozoid/X" ii 6 0 #LFO3 on curvenumber 0 (lissajous)
oscsend 127.0.0.1 8005 "/nozoid/Y" ii 7 0 #ADSR on curvenumber 0

oscsend 127.0.0.1 8005 "/nozoid/Y" ii 6 2 #LFO3
oscsend 127.0.0.1 8005 "/nozoid/X" ii 7 2 #ADSR

oscsend 127.0.0.1 8005 "/nozoid/X" ii 0 1 #None
oscsend 127.0.0.1 8005 "/nozoid/X" ii 0 3 #None
oscsend 127.0.0.1 8005 "/nozoid/Y" ii 0 1 #None
oscsend 127.0.0.1 8005 "/nozoid/Y" ii 0 3 #None
oscsend 127.0.0.1 8005 "/nozoid/color" iiii 0 0 255 0
oscsend 127.0.0.1 8005 "/nozoid/color" iiii 255 0 0 2
