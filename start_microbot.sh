#! /bin/bash
while true
do
   nohup python3 /opt/adex_microbot/main.py >> /root/main.log
   sleep 180
done
