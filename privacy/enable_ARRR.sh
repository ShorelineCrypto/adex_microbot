#! /bin/bash

source /root/atomicDEX-API/target/debug/userpass

curl --url "http://127.0.0.1:7783" --data "{\"userpass\":\"${userpass}\",\"method\":\"task::enable_z_coin::init\",\"mmrpc\":\"2.0\",\"params\":{\"ticker\":\"ARRR\",\"activation_params\":{\"mode\":{\"rpc\":\"Light\",\"rpc_data\":{\"electrum_servers\":[{\"url\":\"electrum1.cipig.net:10008\"},{\"url\":\"electrum2.cipig.net:10008\"},{\"url\":\"electrum3.cipig.net:10008\"}],\"light_wallet_d_servers\":[\"https://electrum1.cipig.net:9447\",\"https://electrum2.cipig.net:9447\",\"https://electrum3.cipig.net:9447\"]}},\"scan_interval_ms\":1000}}}"
