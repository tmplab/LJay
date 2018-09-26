#!/bin/bash
if [[ -z $1 ]]
then
 VAL=0
else
 VAL=$1
fi

oscsend 127.0.0.1 8003 "/nozoid/up" i $VAL
