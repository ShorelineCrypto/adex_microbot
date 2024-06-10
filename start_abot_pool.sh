#! /bin/bash

while true
do
   nohup python3 /opt/adex_microbot/abot_pool.py > /root/pool.log
   sleep 180
done
