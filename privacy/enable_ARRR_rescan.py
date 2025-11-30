#!/usr/bin/env python3
import os
import sys
import time
import json
import requests
from dotenv import load_dotenv
import argparse

def main(args):
    load_dotenv()
    USERPASS = os.getenv("userpass")
    if not USERPASS:
        print("USERPASS not set! Set it in a .env file in this folder. For more information, refer to https://help.pythonanywhere.com/pages/environment-variables-for-web-apps/")
        USERPASS = input("Enter your userpass: ")

    if args.days is None:
        sys.exit("ERROR: must provide past number of days (integer) to rescan Pirate Chain ARRR blockchain")

    current_unix_time = int(time.time())
    scan_date = current_unix_time - (args.days * 24 * 60 * 60)

    params = {
            "userpass": "RPC_UserP@SSW0RD",
            "method": "task::enable_z_coin::init",
            "mmrpc": "2.0",
            "params": {
                "ticker": "ARRR",
                "activation_params": {
                    "mode": {
                        "rpc": "Light",
                        "rpc_data": {
                           "electrum_servers":[
                               { "url": "electrum1.cipig.net:10008"},
                               { "url": "electrum2.cipig.net:10008"},
                               { "url": "electrum3.cipig.net:10008"}
                           ],
                            "light_wallet_d_servers": [
                                "https://electrum1.cipig.net:9447",
                                "https://electrum2.cipig.net:9447",
                                "https://electrum3.cipig.net:9447"],
                            "sync_params": {
                                "date": 1672704000
                            }
                        }
                    },
                    "scan_interval_ms": 1000
                }
            }
    }

    params.update({"userpass": USERPASS})
    params["params"]["activation_params"]["mode"]["rpc_data"]["sync_params"]["date"] = scan_date

    response = requests.post('http://127.0.0.1:7783', json.dumps(params)).json()
    print(response)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--days', type=int, nargs='?',
                        help='number of past days to rescan ARRR blockchain ')
    args = parser.parse_args()
    # running main function
    main(args)