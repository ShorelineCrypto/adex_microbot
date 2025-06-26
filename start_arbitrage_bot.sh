#! /bin/bash

while true
do
   ## allow CEX nonkyc trade to finish in 10 minutes to avoid duplicate trades
   timeout 600 python3 /opt/adex_microbot/arbitrage.py 2>&1 > /root/arb.log &
   sleep 180
done
