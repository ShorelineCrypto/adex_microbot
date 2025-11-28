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

    if args.address is None:
        sys.exit("ERROR: must provide Pirate Chain ARRR withdraw address")
    if args.amount is None:
        sys.exit("ERROR: must provide ARRR withdraw amount")

    params = {
            "mmrpc": "2.0",
            "userpass": "RPC_UserP@SSW0RD",
            "method": "task::withdraw::init",
            "params": {
                "coin": "ARRR",
                "to": "RECIPIENT_ADDRESS",
                "amount": "AMOUNT"
            },
            "id": 0
    }

    params.update({"userpass": USERPASS})
    params["params"]["to"] = str(args.address)
    params["params"]["amount"] = str(args.amount)

    response = requests.post('http://127.0.0.1:7783', json.dumps(params)).json()
    print(response)
    task_id = response["result"]["task_id"]

    params2 = {
        "mmrpc": "2.0",
        "userpass": "RPC_UserP@SSW0RD",
        "method": "task::withdraw::status",
        "params": {
            "task_id": 1,
            "forget_if_finished": False
        },
        "id": 0
    }
    params2.update({"userpass": USERPASS})
    params2["params"]["task_id"] = int(task_id)
    response2 = requests.post('http://127.0.0.1:7783', json.dumps(params2)).json()
    print(response2)
    tx_hex = None
    if response2["result"]["status"] == "Ok":
        tx_hex = response2["result"]["details"]["tx_hex"]
    else:
        # allow slow machine to wait up to 30 minutes to finish
        for i in range(0, 1800):
            time.sleep(1)
            response2 = requests.post('http://127.0.0.1:7783', json.dumps(params2)).json()
            if response2["result"]["status"] == "Ok":
                tx_hex = response2["result"]["details"]["tx_hex"]
                break
    if response2["result"]["status"] != "Ok":
        sys.exit("ERROR: task::withdraw::status failed, id: 0, task_id: {}".format(str(task_id)))

    params3 = {
        "userpass": "RPC_UserP@SSW0RD",
        "method": "send_raw_transaction",
        "coin": "ARRR",
        "tx_hex": "RAW_TX_HEX"
    }
    params3.update({"userpass": USERPASS})
    params3.update({"tx_hex": tx_hex})
    response3 = requests.post('http://127.0.0.1:7783', json.dumps(params3)).json()
    print(response3)
    print("withdraw {} ARRR to {} completed".format(args.amount, args.address))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--amount', type=float, nargs='?',
                        help='withraw ARRR amount ')
    parser.add_argument('--address', nargs='?', type=str,
                        help='Destination ARRR address')

    args = parser.parse_args()
    # running main function
    main(args)