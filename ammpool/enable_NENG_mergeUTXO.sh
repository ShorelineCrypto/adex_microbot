#!/bin/bash
source /root/atomicDEX-API/target/debug/userpass
curl --url "http://127.0.0.1:7783" --data "{\"method\":\"electrum\",\"coin\":\"NENG\",\"servers\":[{\"url\":\"electrum.shorelinecrypto.com:10001\"},{\"url\":\"electrum.blastinvest.com:10001\"},{\"url\":\"electrum2.mooo.com:10001\"}],\"min_connected\":1,\"max_connected\":2,\"userpass\":\"$userpass\",\"mm2\":1,\"requires_notarization\":false,\"required_confirmations\":2,\"utxo_merge_params\":{\"merge_at\":70,\"check_every\":3600,\"max_merge_at_once\":50}}"
