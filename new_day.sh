#!/bin/sh

day=$(ls src/day* | sed 's/src\/day\(\w\+\).py/\1/' | sort -n | tail -n1 )
day=$((day + 1))
if [ ! -d "src/day$day" ]; then
    cp template.py src/day$day.py
    chmod +x src/day$day.py
    sed -i "s/dayx/day$day/" src/day$day.py
    touch inputs/day$day
fi
