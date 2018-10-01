#!/bin/bash
oscsend 127.0.0.1 8005 "/nozoid/X" ii 20 0 #audio_outR
oscsend 127.0.0.1 8005 "/nozoid/Y" ii 21 0 #audio_outL

oscsend 127.0.0.1 8005 "/nozoid/X" ii 21 2 #audio_outL
oscsend 127.0.0.1 8005 "/nozoid/Y" ii 20 2 #audio_outR

oscsend 127.0.0.1 8005 "/nozoid/X" ii 0 1 #None
oscsend 127.0.0.1 8005 "/nozoid/Y" ii 0 1 #None

oscsend 127.0.0.1 8005 "/nozoid/X" ii 0 3 #None
oscsend 127.0.0.1 8005 "/nozoid/Y" ii 0 3 #None

oscsend 127.0.0.1 8005 "/nozoid/color" iiii 0 0 255 0
oscsend 127.0.0.1 8005 "/nozoid/color" iiii 255 0 0 2
