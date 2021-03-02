#!/usr/bin/env bash

rsync -r lib main.py pi@$1:/home/pi/code/e-paper-frame
