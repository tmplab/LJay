#!/bin/bash
myvar=$(lsusb | grep "Bus $1 Device $2" | sed 's/\// /' | awk '{for(i=7;i<=NF;++i)print $i}')
echo $myvar