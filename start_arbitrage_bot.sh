#! /bin/bash

while true
do
   timeout 170 python3 /opt/adex_microbot/arbitrage.py 2>&1 > /root/arb.log &
   sleep 180
done
