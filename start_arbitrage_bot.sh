#! /bin/bash

while true
do
   nohup python3 /opt/adex_microbot/arbitrage.py > /root/arb.log &
   sleep 180
done
