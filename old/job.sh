#!/bin/bash
counter=0
while [ $counter -le 99 ]
do
python sim.py
((counter++))
done
echo ALL done
