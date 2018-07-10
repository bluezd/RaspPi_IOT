#!/bin/bash

make clean -C temperature > /dev/null 2>&1
make -C temperature > /dev/null 2>&1

sudo ln -s `pwd`/temperature/TEM_HUM /usr/local/bin/TEM_HUM
