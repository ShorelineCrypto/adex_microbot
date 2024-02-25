#!/usr/bin/env python3
import os
import sys
import json
import time
import mnemonic
import requests
import pykomodefi
import subprocess
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

def main():
    current_prices = get_prices()

    NENG_KMD_price = float(current_prices["NENG"]["last_price"]) / float(current_prices["KMD"]["last_price"])
    CHTA_KMD_price = float(current_prices["CHTA"]["last_price"]) / float(current_prices["KMD"]["last_price"])
    print (" NENG/KMD mkt price: {}\t CHTA/KMD mkt price: {}".format(str(NENG_KMD_price), str(CHTA_KMD_price)))
    # trading pair min_usd = $0.05
    NENG_unit = round ((0.05 / float(current_prices["NENG"]["last_price"])), 4)
    CHTA_unit = round ((0.05 / float(current_prices["CHTA"]["last_price"])), 4)
    base_spread = 0.01
    print ("/root/mmtools/cancel_all_orders")
    result = subprocess.run("/root/mmtools/cancel_all_orders", shell=True)


    for i in range(1, 4):
        spread = base_spread * i
        print("/root/mmtools/buy CHTA KMD {} {}".format((CHTA_KMD_price / (1 + spread)), CHTA_unit))
        result = subprocess.run("/root/mmtools/buy CHTA KMD {} {}".format((CHTA_KMD_price / (1 + spread)), CHTA_unit), shell=True)
        print("/root/mmtools/sell CHTA KMD {} {}".format((CHTA_KMD_price * (1 + spread)), CHTA_unit))
        result = subprocess.run("/root/mmtools/sell CHTA KMD {} {}".format((CHTA_KMD_price * (1 + spread)), CHTA_unit), shell=True)
    
        print("/root/mmtools/buy NENG KMD {} {}".format((NENG_KMD_price / (1 + spread)), NENG_unit))
        result = subprocess.run("/root/mmtools/buy NENG KMD {} {}".format((NENG_KMD_price / (1 + spread)), NENG_unit), shell=True)
        print("/root/mmtools/sell NENG KMD {} {}".format((NENG_KMD_price * (1 + spread)), NENG_unit))
        result = subprocess.run("/root/mmtools/sell NENG KMD {} {}".format((NENG_KMD_price * (1 + spread)), NENG_unit), shell=True)


    ## start DGB pair on new MM2 scripts, mmtool not used
    os.chdir('/root/atomicDEX-API/target/debug')
    print("path changed to /root/atomicDEX-API/target/debug")

    NENG_DGB_price = float(current_prices["NENG"]["last_price"]) / float(current_prices["DGB"]["last_price"])
    DGB_NENG_price = float(current_prices["DGB"]["last_price"]) / float(current_prices["NENG"]["last_price"])
    print (" NENG/DGB mkt price: {}\t DGB/NENG mkt price: {}".format(str(NENG_DGB_price), str(DGB_NENG_price)))
    CHTA_DGB_price = float(current_prices["CHTA"]["last_price"]) / float(current_prices["DGB"]["last_price"])
    DGB_CHTA_price = float(current_prices["DGB"]["last_price"]) / float(current_prices["CHTA"]["last_price"])
       
    # trading pair min_usd = $0.05, NENG_unit CHTA_unit unchanged
    DGB_unit =  round ((0.05 / float(current_prices["DGB"]["last_price"])), 8)

    # use new komododif scripts to support DGB-segwit
    for i in range(1, 4):
        spread = base_spread * i
    
        print("./place_order.sh NENG DGB-segwit {} {} | jq '.'".format((NENG_DGB_price * (1 + spread)), NENG_unit))
        result = subprocess.run("./place_order.sh NENG DGB-segwit {} {} | jq '.'".format((NENG_DGB_price * (1 + spread)), NENG_unit), shell=True)
        print("./place_order.sh DGB-segwit NENG {} {} | jq '.'".format((DGB_NENG_price * (1 + spread)), DGB_unit))
        result = subprocess.run("./place_order.sh DGB-segwit NENG {} {} | jq '.'".format((DGB_NENG_price * (1 + spread)), DGB_unit), shell=True)


if __name__ == "__main__":
    main()
