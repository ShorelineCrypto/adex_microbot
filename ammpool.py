#!/usr/bin/env python3
import os
import sys
import json
import time
import mnemonic
import requests
import pykomodefi
import subprocess
import argparse
import re
from const import (
    ACTIVE_TASKS,
    USERPASS_FILE,
    PRICES_URL,
    ERROR_EVENTS,
    BOT_PARAMS_FILE,
    BOT_SETTINGS_FILE,
    ACTIVATE_COMMANDS,
    MM2_LOG_FILE,
    MM2BIN,
    MM2_JSON_FILE,
    COINS_LIST
)
from helpers import (
    color_input,
    success_print,
    status_print,
    table_print,
    error_print,
    sleep_message,
    preexec,
    get_mm2,
    get_price,
    get_order_count,
    get_valid_input,
    sec_to_hms,
    generate_rpc_pass,
    get_prices
)

from models import Dex, Table, Config

dex = Dex()
tables = Table()

coins_list = dex.enabled_coins_list

if len(coins_list) == 0:
    status_print("No coins are activated!")
else:
    # Documentation: https://developers.komodoplatform.com/basic-docs/atomicdex/atomicdex-api-legacy/my_balance.html
    tables.balances(coins_list)


class coinBalance:
    def __init__(self):
        self.config = Config()
        self.dex = Dex()

    def balance(self, coin=None):
            total_value = 0
            resp = Dex().get_balance(coin)
            if "balance" in resp:
                total_balance = float(resp["balance"]) + float(
                    resp["unspendable_balance"]
                )
                return total_balance
            else:
                print(resp)
                return None


def main(args):
    spread = args.base_spread
 
    [coin, othercoin] = re.split('/', args.market)
    print (" {} mkt pairs {} {}".format(args.market, coin, othercoin))
    
    while True:
    
        cb = coinBalance()
    
        coin_balance = coinBalance.balance(cb,coin=coin)
        othercoin_balance = coinBalance.balance(cb,coin=othercoin)
        print (" {} balance: {} .  {} balance: {}".format(coin, str(coin_balance), othercoin, str(othercoin_balance)))
    
        coin_othercoin_price = othercoin_balance / coin_balance
        print (" {} mkt price: {}".format(args.market, str(coin_othercoin_price)))
        # trading pair amount for NENG is 
        coin_unit = round (coin_balance * args.ordersize, 8)
        # trading pair amount for KMD is
        othercoin_unit = round (othercoin_balance * args.ordersize, 8)
        othercoin_coin_price = coin_balance / othercoin_balance 

        print ("/root/mmtools/cancel_all_orders")
        result = subprocess.run("/root/mmtools/cancel_all_orders", shell=True)

        ## start AMM pair on new MM2 scripts, mmtool not used
        os.chdir('/root/atomicDEX-API/target/debug')
        print("path changed to /root/atomicDEX-API/target/debug")
    
        print("./place_fastorder.sh {} {} {} {} | jq '.'".format(coin, othercoin, (coin_othercoin_price * (1 + spread)), coin_unit))
        result = subprocess.run("./place_fastorder.sh {} {} {} {} | jq '.'".format(coin, othercoin, (coin_othercoin_price * (1 + spread)), coin_unit), shell=True)
        print("./place_fastorder.sh {} {} {} {} | jq '.'".format(othercoin, coin, (othercoin_coin_price * (1 + spread)), othercoin_unit))
        result = subprocess.run("./place_fastorder.sh {} {} {} {} | jq '.'".format(othercoin, coin, (othercoin_coin_price * (1 + spread)), othercoin_unit), shell=True)
        
        time.sleep(args.interval)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--base_spread', nargs='?', type=float, default=0.0045 ,
                        help='base spread in fraction from mkt price [default: 0.0045]')
    parser.add_argument('--market', nargs='?', type=str, default='NENG/KMD' ,
                        help='market [default: NENG/KMD]')
    parser.add_argument('--interval', nargs='?', type=float, default=180.0,
                        help='refresh interval rate on orders in seconds[default: 180.0]')
    parser.add_argument('--ordersize', nargs='?', type=float, default=0.002,
                        help='size of open orders in fraction of liquidity pool[default: 0.002]')
    args = parser.parse_args()
    
    # running main function
    main(args)
