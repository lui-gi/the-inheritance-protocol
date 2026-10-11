#!/bin/sh
# Asks the porch sensor how many pumpkins it can see. Seasonal.
mosquitto_sub -h 10.13.0.2 -t house/porch/objects -C 1 | grep -c pumpkin
