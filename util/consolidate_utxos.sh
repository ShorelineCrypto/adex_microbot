#!/bin/bash
if [ "$#" -lt 1 ]; then
          echo "Usage: $0 <coin> (<merge_at, default=70> <max_merge_at_once, default=50>)"
          exit 1
fi

MERGEAT="${2:-70}"
MAXMERGE="${3:-50}"

source /root/atomicDEX-API/target/debug/userpass
curl --url "http://127.0.0.1:7783" --data "{\"userpass\":\"$userpass\",\"method\":\"consolidate_utxos\",\"mmrpc\":\"2.0\",\"params\":{\"coin\":\"$1\",\"broadcast\":true,\"merge_conditions\": {\"merge_at\": $MERGEAT,\"max_merge_at_once\":$MAXMERGE}}}"

echo
