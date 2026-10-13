#!/usr/bin/env bash

ssh rpi-4@10.120.39.106 "nohup pi_record > /dev/null 2>&1 &"