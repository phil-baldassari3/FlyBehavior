#!/usr/bin/env bash

ssh rpi-5@10.120.39.105 "nohup pi_record > /dev/null 2>&1 &"
