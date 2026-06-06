#!/bin/bash
source /root/atomicDEX-API/target/debug/userpass
curl --url "http://127.0.0.1:7783" --data "{\"method\":\"electrum\",\"coin\":\"FIRO\",\"servers\":[{\"url\":\"electrumx.firo.org:50001\"},{\"url\":\"electrumx01.firo.org:50001\"},{\"url\":\"electrumx02.firo.org:50001\"},{\"url\":\"electrumx03.firo.org:50001\"}],\"min_connected\":1,\"max_connected\":2,\"userpass\":\"$userpass\",\"mm2\":1,\"requires_notarization\":false,\"required_confirmations\":2,\"utxo_merge_params\":{\"merge_at\":70,\"check_every\":3600,\"max_merge_at_once\":50}}"
