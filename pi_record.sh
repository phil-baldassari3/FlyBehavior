#!/usr/bin/env bash

# Template script to run record_copulation_assay.py on a raspberry pi 
# with the correct Len Position and Directory arguments

date_stamp=`date -I`

prefix="/home/rpi-0/Desktop/pi_record_stdout_stderr/${date_stamp}"

record_copulation_assay.py <len position> <path/to/save/direcoty> \
    > "${prefix}_stdout.txt" \
    2> "${prefix}_stderr.txt"