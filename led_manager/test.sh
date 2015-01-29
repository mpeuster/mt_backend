#!/bin/bash

python libledbulbs.py -a on -g 1
sleep 1
python libledbulbs.py -a on -g 2
sleep 1
python libledbulbs.py -a on -g 3
sleep 1
python libledbulbs.py -a on -g 4
sleep 1

python libledbulbs.py -a color -g 1 -c red
sleep 1
python libledbulbs.py -a color -g 2 -c blue
sleep 1
python libledbulbs.py -a color -g 3 -c yellow
sleep 1
python libledbulbs.py -a color -g 4 -c pink
sleep 1


sleep 1
python libledbulbs.py -a color -c green
sleep 2

python libledbulbs.py -a off