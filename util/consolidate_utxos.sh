#!/bin/bash
if [ "$#" -ne 1 ]; then
          echo "Usage: $0 <coin symbol>"
            exit 1
fi

source /root/atomicDEX-API/target/debug/userpass
curl --url "http://127.0.0.1:7783" --data "{\"userpass\":\"$userpass\",\"method\":\"consolidate_utxos\", \"mmrpc\": \"2.0\",
          \"params\": {
          \"coin\": \"$1\",
          \"merge_conditions\": {
            \"merge_at\": 70,
            \"max_merge_at_once\": 50,
        },
        \"broadcast\": true
        }}"
