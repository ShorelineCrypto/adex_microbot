#! /bin/bash

while true
do
   nohup timeout 179 python3 /opt/adex_microbot/abot_pool.py --NENGCHTA_POOL True > /root/pool.log &
   sleep 180
done
