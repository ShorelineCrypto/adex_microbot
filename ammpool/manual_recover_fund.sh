#!/bin/bash
if [ "$#" -ne 1 ]; then
          echo "Usage: $0 <uuid>"
            exit 1
fi

source /root/atomicDEX-API/target/debug/userpass
curl --url "http://127.0.0.1:7783" --data "{\"userpass\":\"$userpass\",\"method\":\"recover_funds_of_swap\",\"params\": {\"uuid\": \"$1\" }}"
