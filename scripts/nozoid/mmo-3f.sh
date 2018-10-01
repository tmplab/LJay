#!/bin/bash
oscsend 127.0.0.1 8005 "/nozoid/X" ii 4 0 #LFO1
oscsend 127.0.0.1 8005 "/nozoid/Y" ii 5 0 #LFO2

oscsend 127.0.0.1 8005 "/nozoid/X" ii 5 2 #LFO2
oscsend 127.0.0.1 8005 "/nozoid/Y" ii 4 2 #LFO1

oscsend 127.0.0.1 8005 "/nozoid/X" ii 0 1 #None
oscsend 127.0.0.1 8005 "/nozoid/Y" ii 0 1 #None

oscsend 127.0.0.1 8005 "/nozoid/X" ii 0 3 #None
oscsend 127.0.0.1 8005 "/nozoid/Y" ii 0 3 #None

oscsend 127.0.0.1 8005 "/nozoid/color" iiii 0 0 255 0
oscsend 127.0.0.1 8005 "/nozoid/color" iiii 255 0 0 2
