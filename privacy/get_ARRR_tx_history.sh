#! /bin/bash
source /root/atomicDEX-API/target/debug/userpass

curl --url "http://127.0.0.1:7783" --data "{
  \"userpass\": \"${userpass}\",
  \"method\": \"z_coin_tx_history\",
  \"mmrpc\": \"2.0\",
  \"params\": {
    \"coin\": \"ARRR\",
    \"limit\": 2,
    \"paging_options\": {
        \"PageNumber\": 2
              }
   }
}"

echo

