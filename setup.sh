#!/bin/bash

make clean -C temperature > /dev/null 2>&1
make -C temperature > /dev/null 2>&1

Target="/usr/local/bin/TEM_HUM"

if [[ -L $Target ]]; then
	sudo rm -rf $Target
fi

sudo ln -s `pwd`/temperature/TEM_HUM $Target || RES=$?
if [[ ! $RES ]]; then
	echo "Done."
	exit 0
else
	echo "$Target already exists, please rename or remove it manually and then run setup.sh again!"
	exit 1
fi
