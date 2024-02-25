#! /bin/bash
while true
do
   nohup python3 /opt/adex_microbot/main_legacy.py > /root/main_legacy.log
   sleep 180
done
