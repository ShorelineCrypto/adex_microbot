#! /bin/bash
source /root/atomicDEX-API/target/debug/userpass

curl --url "http://127.0.0.1:7783" --data "{
  \"userpass\": \"${userpass}\",
  \"method\": \"active_swaps\"
}"

echo
