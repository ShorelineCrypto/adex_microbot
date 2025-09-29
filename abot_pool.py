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
    PRICE_URLS,
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
    CHTA_KMD_price = float(current_prices["CHTA"]["last_price"]) / float(current_prices["KMD"]["last_price"])
    print (" NENG/KMD mkt price: {}\t CHTA/KMD mkt price: {}".format(str(NENG_KMD_price), str(CHTA_KMD_price)))
    # trading pair min_usd = $0.05
    NENG_unit = round ((USD_unit / float(current_prices["NENG"]["last_price"])), 4)
    CHTA_unit = round ((USD_unit / float(current_prices["CHTA"]["last_price"])), 4)

    print ("/root/mmtools/cancel_all_orders")
    result = subprocess.run("/root/mmtools/cancel_all_orders", shell=True)


    for i in range(1, 4):
        spread = base_spread * i
        print("/root/mmtools/fastbuy CHTA KMD {} {}".format((CHTA_KMD_price / (1 + spread)), (CHTA_unit * i)))
        result = subprocess.run("/root/mmtools/fastbuy CHTA KMD {} {}".format((CHTA_KMD_price / (1 + spread)), (CHTA_unit * i)), shell=True)
        print("/root/mmtools/fastsell CHTA KMD {} {}".format((CHTA_KMD_price * (1 + spread)), (CHTA_unit * i)))
        result = subprocess.run("/root/mmtools/fastsell CHTA KMD {} {}".format((CHTA_KMD_price * (1 + spread)), (CHTA_unit * i)), shell=True)
    
        print("/root/mmtools/fastbuy NENG KMD {} {}".format((NENG_KMD_price / (1 + spread)), (NENG_unit * i)))
        result = subprocess.run("/root/mmtools/fastbuy NENG KMD {} {}".format((NENG_KMD_price / (1 + spread)), (NENG_unit * i)), shell=True)
        print("/root/mmtools/fastsell NENG KMD {} {}".format((NENG_KMD_price * (1 + spread)), (NENG_unit * i)))
        result = subprocess.run("/root/mmtools/fastsell NENG KMD {} {}".format((NENG_KMD_price * (1 + spread)), (NENG_unit * i)), shell=True)


    ## start DGB pair on new MM2 scripts, mmtool not used
    os.chdir('/root/atomicDEX-API/target/debug')
    print("path changed to /root/atomicDEX-API/target/debug")

    NENG_DGB_price = float(current_prices["NENG"]["last_price"]) / float(current_prices["DGB"]["last_price"])
    DGB_NENG_price = float(current_prices["DGB"]["last_price"]) / float(current_prices["NENG"]["last_price"])
    print (" NENG/DGB mkt price: {}\t DGB/NENG mkt price: {}".format(str(NENG_DGB_price), str(DGB_NENG_price)))
    CHTA_DGB_price = float(current_prices["CHTA"]["last_price"]) / float(current_prices["DGB"]["last_price"])
    DGB_CHTA_price = float(current_prices["DGB"]["last_price"]) / float(current_prices["CHTA"]["last_price"])
    print (" CHTA/DGB mkt price: {}\t DGB/CHTA mkt price: {}".format(str(CHTA_DGB_price), str(DGB_CHTA_price)))
           
    ## trading pair min_usd = $0.05, NENG_unit CHTA_unit unchanged
    DGB_unit =  round ((USD_unit / float(current_prices["DGB"]["last_price"])), 8)

    if args.USDT_POOL:
        # USDT pair in nonKYC exchange is less liquid. Use Doge pair converted price instead as below
        NENG_USDT_price = float(current_prices["NENG"]["last_price"]) / float(current_prices["USDT"]["last_price"])
        USDT_NENG_price = float(current_prices["USDT"]["last_price"]) / float(current_prices["NENG"]["last_price"])
        print (" NENG/USDT mkt price: {}\t USDT/NENG mkt price: {}".format(str(NENG_USDT_price), str(USDT_NENG_price)))
        CHTA_USDT_price = float(current_prices["CHTA"]["last_price"]) / float(current_prices["USDT"]["last_price"])
        USDT_CHTA_price = float(current_prices["USDT"]["last_price"]) / float(current_prices["CHTA"]["last_price"])
        print (" CHTA/USDT mkt price: {}\t USDT/CHTA mkt price: {}".format(str(CHTA_USDT_price), str(USDT_CHTA_price)))
        USDT_unit = USD_unit

    if args.NENGCHTA_POOL:
        NENG_CHTA_price = float(current_prices["NENG"]["last_price"]) / float(current_prices["CHTA"]["last_price"])
        CHTA_NENG_price = float(current_prices["CHTA"]["last_price"]) / float(current_prices["NENG"]["last_price"])
        print (" NENG/CHTA mkt price: {}\t CHTA/NENG mkt price: {}".format(str(NENG_CHTA_price), str(CHTA_NENG_price)))

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

        if args.USDT_POOL:
            print("./place_order.sh CHTA USDT-PLG20 {} {} | jq '.'".format((CHTA_USDT_price * (1 + spread)), (CHTA_unit * 3)))
            result = subprocess.run("./place_order.sh CHTA USDT-PLG20 {} {} | jq '.'".format((CHTA_USDT_price * (1 + spread)), (CHTA_unit * 3)), shell=True)
            print("./place_order.sh USDT-PLG20 CHTA {} {} | jq '.'".format((USDT_CHTA_price * (1 + spread)), (USDT_unit * 3)))
            result = subprocess.run("./place_order.sh USDT-PLG20 CHTA {} {} | jq '.'".format((USDT_CHTA_price * (1 + spread)), (USDT_unit * 3)), shell=True)

            ## to avoid identical buy / sell price on NENG/USDT on -+1% spread, additional +0.5% spread added, making the total bid/ask spread 2.5% 
            print("./place_order.sh NENG USDT-PLG20 {} {} | jq '.'".format((NENG_USDT_price * (1 + spread + 0.005)), (NENG_unit * 3)))
            result = subprocess.run("./place_order.sh NENG USDT-PLG20 {} {} | jq '.'".format((NENG_USDT_price * (1 + spread + 0.005)), (NENG_unit * 3)), shell=True)
            print("./place_order.sh USDT-PLG20 NENG {} {} | jq '.'".format((USDT_NENG_price * (1 + spread)), (USDT_unit * 3)))
            result = subprocess.run("./place_order.sh USDT-PLG20 NENG {} {} | jq '.'".format((USDT_NENG_price * (1 + spread)), (USDT_unit * 3)), shell=True)
        
        if args.NENGCHTA_POOL:
            # NENG/CHTA pool use fixed $10 USD size and 2% spread
            USD_unit = 10.0
            spread = 0.02
            # trading pair USD = $10
            NENG_unit = round ((USD_unit / float(current_prices["NENG"]["last_price"])), 4)
            CHTA_unit = round ((USD_unit / float(current_prices["CHTA"]["last_price"])), 4)
            print("./place_order.sh NENG CHTA {} {} | jq '.'".format((NENG_CHTA_price * (1 + spread)), NENG_unit))
            result = subprocess.run("./place_order.sh NENG CHTA {} {} | jq '.'".format((NENG_CHTA_price * (1 + spread)), NENG_unit), shell=True)
            print("./place_order.sh CHTA NENG {} {} | jq '.'".format((CHTA_NENG_price * (1 + spread)), CHTA_unit))
            result = subprocess.run("./place_order.sh CHTA NENG {} {} | jq '.'".format((CHTA_NENG_price * (1 + spread)), CHTA_unit), shell=True)

        

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--usd_unit', type=float, nargs='?', default=0.05 , 
                        help='USD_unit - trading amount on USD worth, [default: 0.05]')
    parser.add_argument('--base_spread', nargs='?', type=float, default=0.01 ,
                        help='base spread in fraction from mkt price [default: 0.01]')
    parser.add_argument('--USDT_POOL', nargs='?', type=bool, default=False ,
                        help='enable USDT-PLG20 pool [default: False]')
    parser.add_argument('--NENGCHTA_POOL', nargs='?', type=bool, default=False ,
                        help='enable NENG-CHTA pool [default: False]')
    args = parser.parse_args()
    # running main function
    main(args)
