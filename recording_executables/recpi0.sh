#!/usr/bin/env bash

ssh rpi-0@10.120.38.220 "nohup pi_record > /dev/null 2>&1 &"
