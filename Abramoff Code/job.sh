#!/bin/bash

counter=0
trap "exit" INT
while [ $counter -le 99 ]
do
python sim.py
((counter++))
done
echo ALL done
