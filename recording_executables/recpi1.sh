#!/usr/bin/env bash

ssh rpi-1@10.120.39.111 "nohup pi_record > /dev/null 2>&1 &"
