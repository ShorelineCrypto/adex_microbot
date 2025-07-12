#! /bin/bash

while true
do
   timeout 170 python3 /opt/adex_microbot/abot_pool.py --USDT_POOL True  2>&1 > /root/pool.log &
   sleep 180
done
