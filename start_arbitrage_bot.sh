#! /bin/bash

while true
do
   ## allow CEX nonkyc trade to finish in 30 minutes to avoid duplicate trades
   timeout 1800 python3 /opt/adex_microbot/arbitrage.py --usd_unit 10.0 --min_cex_usd_unit 1.4 2>&1 >> /root/arb.log &
   sleep 180
done
