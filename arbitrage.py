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

def main(args):
    current_prices = get_prices()
    USD_unit = args.usd_unit
    base_spread = args.base_spread

    NENG_KMD_price = float(current_prices["NENG"]["last_price"]) / float(current_prices["KMD"]["last_price"])
    KMD_NENG_price = float(current_prices["KMD"]["last_price"]) / float(current_prices["NENG"]["last_price"])
    CHTA_KMD_price = float(current_prices["CHTA"]["last_price"]) / float(current_prices["KMD"]["last_price"])
    KMD_CHTA_price = float(current_prices["KMD"]["last_price"]) / float(current_prices["CHTA"]["last_price"])
    print (" NENG/KMD mkt price: {}\t CHTA/KMD mkt price: {}".format(str(NENG_KMD_price), str(CHTA_KMD_price)))
    # trading pair min_usd = $1.0
    NENG_unit = round ((USD_unit / float(current_prices["NENG"]["last_price"])), 4)
    CHTA_unit = round ((USD_unit / float(current_prices["CHTA"]["last_price"])), 4)

    NENG_DGB_price = float(current_prices["NENG"]["last_price"]) / float(current_prices["DGB"]["last_price"])
    DGB_NENG_price = float(current_prices["DGB"]["last_price"]) / float(current_prices["NENG"]["last_price"])
    print (" NENG/DGB mkt price: {}\t DGB/NENG mkt price: {}".format(str(NENG_DGB_price), str(DGB_NENG_price)))
    CHTA_DGB_price = float(current_prices["CHTA"]["last_price"]) / float(current_prices["DGB"]["last_price"])
    DGB_CHTA_price = float(current_prices["DGB"]["last_price"]) / float(current_prices["CHTA"]["last_price"])
    print (" CHTA/DGB mkt price: {}\t DGB/CHTA mkt price: {}".format(str(CHTA_DGB_price), str(DGB_CHTA_price)))
       
    DGB_unit = round ((USD_unit / float(current_prices["DGB"]["last_price"])), 8)
    KMD_unit = round ((USD_unit / float(current_prices["KMD"]["last_price"])), 8)
    
    print ("/root/mmtools/cancel_all_orders")
    result = subprocess.run("/root/mmtools/cancel_all_orders", shell=True)

    ## start DGB pair on new MM2 scripts, mmtool not used
    os.chdir('/root/atomicDEX-API/target/debug')
    print("path changed to /root/atomicDEX-API/target/debug")
    
    ## use new komododif scripts to support DGB-segwit
    ## the setprice will overwrite old order, one order pair only
    ## setprice in place_order.sh is sell always
    for j in range(1, 2):
        spread = base_spread * j
    
        print("./place_order.sh CHTA DGB-segwit {} {} | jq '.'".format((CHTA_DGB_price * (1 + spread)), CHTA_unit))
        result = subprocess.run("./place_order.sh CHTA DGB-segwit {} {} | jq '.'".format((CHTA_DGB_price * (1 + spread)), CHTA_unit), shell=True)
        print("./place_order.sh DGB-segwit CHTA {} {} | jq '.'".format((DGB_CHTA_price * (1 + spread)), DGB_unit))
        result = subprocess.run("./place_order.sh DGB-segwit CHTA {} {} | jq '.'".format((DGB_CHTA_price * (1 + spread)), DGB_unit), shell=True)

        print("./place_order.sh NENG DGB-segwit {} {} | jq '.'".format((NENG_DGB_price * (1 + spread)), NENG_unit))
        result = subprocess.run("./place_order.sh NENG DGB-segwit {} {} | jq '.'".format((NENG_DGB_price * (1 + spread)), NENG_unit), shell=True)
        print("./place_order.sh DGB-segwit NENG {} {} | jq '.'".format((DGB_NENG_price * (1 + spread)), DGB_unit))
        result = subprocess.run("./place_order.sh DGB-segwit NENG {} {} | jq '.'".format((DGB_NENG_price * (1 + spread)), DGB_unit), shell=True)

        print("./place_order.sh CHTA KMD {} {} | jq '.'".format((CHTA_KMD_price * (1 + spread)), CHTA_unit))
        result = subprocess.run("./place_order.sh CHTA KMD {} {} | jq '.'".format((CHTA_KMD_price * (1 + spread)), CHTA_unit), shell=True)
        print("./place_order.sh KMD CHTA {} {} | jq '.'".format((KMD_CHTA_price * (1 + spread)), KMD_unit))
        result = subprocess.run("./place_order.sh KMD CHTA {} {} | jq '.'".format((KMD_CHTA_price * (1 + spread)), KMD_unit), shell=True)

        print("./place_order.sh NENG KMD {} {} | jq '.'".format((NENG_KMD_price * (1 + spread)), NENG_unit))
        result = subprocess.run("./place_order.sh NENG KMD {} {} | jq '.'".format((NENG_KMD_price * (1 + spread)), NENG_unit), shell=True)
        print("./place_order.sh KMD NENG {} {} | jq '.'".format((KMD_NENG_price * (1 + spread)), KMD_unit))
        result = subprocess.run("./place_order.sh KMD NENG {} {} | jq '.'".format((KMD_NENG_price * (1 + spread)), KMD_unit), shell=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--usd_unit', type=float, nargs='?', default=1.0 , 
                        help='USD_unit - trading amount on USD worth, [default: 1.0]')
    parser.add_argument('--base_spread', nargs='?', type=spread, default=0.1 ,
                        help='base spread in fraction from mkt price [default: 0.1]')
    
    args = parser.parse_args()
    # running main function
    main(args)