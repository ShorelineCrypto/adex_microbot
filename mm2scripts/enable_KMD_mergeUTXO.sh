#!/bin/bash
source userpass
curl --url "http://127.0.0.1:7783" --data "{\"method\":\"electrum\",\"coin\":\"KMD\",\"servers\":[{\"url\":\"electrum1.cipig.net:10001\"},{\"url\":\"electrum2.cipig.net:10001\"},{\"url\":\"electrum3.cipig.net:10001\"}],\"min_connected\":1,\"max_connected\":2,\"userpass\":\"$userpass\",\"mm2\":1,\"requires_notarization\":false,\"required_confirmations\":2,\"utxo_merge_params\":{\"merge_at\":70,\"check_every\":3600,\"max_merge_at_once\":50}}"
