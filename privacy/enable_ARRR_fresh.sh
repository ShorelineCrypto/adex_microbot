#! /bin/bash

source /root/atomicDEX-API/target/debug/userpass

curl --url "http://127.0.0.1:7783" --data "{\"userpass\":\"${userpass}\",\"method\":\"task::enable_z_coin::init\",\"mmrpc\":\"2.0\",\"params\":{\"ticker\":\"ARRR\",\"activation_params\":{\"mode\":{\"rpc\":\"Light\",\"rpc_data\":{\"electrum_servers\":[{\"url\":\"arrr.electrum1.cipig.net:10008\"},{\"url\":\"arrr.electrum2.cipig.net:10008\"},{\"url\":\"arrr.electrum3.cipig.net:10008\"}],\"light_wallet_d_servers\":[\"https://lightd1.pirate.black:443\",\"https://piratelightd1.cryptoforge.cc:443\",\"https://piratelightd2.cryptoforge.cc:443\",\"https://piratelightd3.cryptoforge.cc:443\",\"https://piratelightd4.cryptoforge.cc:443\",\"https://electrum1.cipig.net:9447\",\"https://electrum2.cipig.net:9447\",\"https://electrum3.cipig.net:9447\"]}},\"scan_interval_ms\":1000}}}"
