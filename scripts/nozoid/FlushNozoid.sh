#!/bin/bash
echo 0xFF |xxd -r > /dev/ttyACM0
echo 0xFF |xxd -r > /dev/ttyACM1
