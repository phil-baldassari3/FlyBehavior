#!/usr/bin/env bash

ssh rpi-2@10.120.39.110 "nohup pi_record > /dev/null 2>&1 &"
