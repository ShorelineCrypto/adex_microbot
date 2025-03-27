#! /bin/bash

while true
do
   nohup timeout 179 python3 /opt/adex_microbot/arbitrage.py > /root/arb.log &
   sleep 180
done
