#!/usr/bin/env bash

ssh rpi-3@10.120.38.39 "nohup pi_record > /dev/null 2>&1 &"
