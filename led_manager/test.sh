#!/bin/bash

python libledbulbs.py -a on -g 1
python libledbulbs.py -a on -g 2
python libledbulbs.py -a on -g 3
python libledbulbs.py -a on -g 4
sleep 1

python libledbulbs.py -a color  -c red
sleep 1
python libledbulbs.py -a color  -c blue
sleep 1
python libledbulbs.py -a color  -c yellow
sleep 1
python libledbulbs.py -a color  -c pink
sleep 1


sleep 1
python libledbulbs.py -a color -c green
sleep 2

python libledbulbs.py -a off
