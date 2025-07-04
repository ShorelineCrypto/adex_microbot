#!/usr/bin/env python3
import os
import sys
import json
import sqlite3
import glob
import re
import time
import mnemonic
import requests
import pykomodefi
import subprocess
import argparse
from nonkyc import NonKYCClient
from decimal import Decimal
import asyncio, signal
from const import (
    SCRIPT_PATH,
    MM2_JSON_FILE,
    PRICES_URL,
)
from helpers import (
    get_prices
)

def main(args):
    global NENG_USDT_price
    global CHTA_USDT_price
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
    
    # USDT pair in nonKYC exchange is less liquid. Use Doge pair converted price instead as below
    NENG_USDT_price = float(current_prices["NENG"]["last_price"]) / float(current_prices["USDT"]["last_price"])
    USDT_NENG_price = float(current_prices["USDT"]["last_price"]) / float(current_prices["NENG"]["last_price"])
    print (" NENG/USDT mkt price: {}\t USDT/NENG mkt price: {}".format(str(NENG_USDT_price), str(USDT_NENG_price)))
    CHTA_USDT_price = float(current_prices["CHTA"]["last_price"]) / float(current_prices["USDT"]["last_price"])
    USDT_CHTA_price = float(current_prices["USDT"]["last_price"]) / float(current_prices["CHTA"]["last_price"])
    print (" CHTA/USDT mkt price: {}\t USDT/CHTA mkt price: {}".format(str(CHTA_USDT_price), str(USDT_CHTA_price)))

    # USDC-PLG20 pair
    NENG_USDC_price = float(current_prices["NENG"]["last_price"]) / float(current_prices["USDC"]["last_price"])
    USDC_NENG_price = float(current_prices["USDC"]["last_price"]) / float(current_prices["NENG"]["last_price"])
    print (" NENG/USDC mkt price: {}\t USDC/NENG mkt price: {}".format(str(NENG_USDC_price), str(USDC_NENG_price)))
    CHTA_USDC_price = float(current_prices["CHTA"]["last_price"]) / float(current_prices["USDC"]["last_price"])
    USDC_CHTA_price = float(current_prices["USDC"]["last_price"]) / float(current_prices["CHTA"]["last_price"])
    print (" CHTA/USDC mkt price: {}\t USDC/CHTA mkt price: {}".format(str(CHTA_USDC_price), str(USDC_CHTA_price)))
       
    DGB_unit = round ((USD_unit / float(current_prices["DGB"]["last_price"])), 8)
    KMD_unit = round ((USD_unit / float(current_prices["KMD"]["last_price"])), 8)
    USDT_unit = USD_unit
    USDC_unit = USD_unit

    
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

        print("./place_fastorder.sh CHTA KMD {} {} | jq '.'".format((CHTA_KMD_price * (1 + spread)), CHTA_unit))
        result = subprocess.run("./place_fastorder.sh CHTA KMD {} {} | jq '.'".format((CHTA_KMD_price * (1 + spread)), CHTA_unit), shell=True)
        print("./place_fastorder.sh KMD CHTA {} {} | jq '.'".format((KMD_CHTA_price * (1 + spread)), KMD_unit))
        result = subprocess.run("./place_fastorder.sh KMD CHTA {} {} | jq '.'".format((KMD_CHTA_price * (1 + spread)), KMD_unit), shell=True)

        print("./place_fastorder.sh NENG KMD {} {} | jq '.'".format((NENG_KMD_price * (1 + spread)), NENG_unit))
        result = subprocess.run("./place_fastorder.sh NENG KMD {} {} | jq '.'".format((NENG_KMD_price * (1 + spread)), NENG_unit), shell=True)
        print("./place_fastorder.sh KMD NENG {} {} | jq '.'".format((KMD_NENG_price * (1 + spread)), KMD_unit))
        result = subprocess.run("./place_fastorder.sh KMD NENG {} {} | jq '.'".format((KMD_NENG_price * (1 + spread)), KMD_unit), shell=True)

        print("./place_order.sh CHTA USDT-PLG20 {} {} | jq '.'".format((CHTA_USDT_price * (1 + spread)), CHTA_unit))
        result = subprocess.run("./place_order.sh CHTA USDT-PLG20 {} {} | jq '.'".format((CHTA_USDT_price * (1 + spread)), CHTA_unit), shell=True)
        print("./place_order.sh USDT-PLG20 CHTA {} {} | jq '.'".format((USDT_CHTA_price * (1 + spread)), USDT_unit))
        result = subprocess.run("./place_order.sh USDT-PLG20 CHTA {} {} | jq '.'".format((USDT_CHTA_price * (1 + spread)), USDT_unit), shell=True)

        print("./place_order.sh NENG USDT-PLG20 {} {} | jq '.'".format((NENG_USDT_price * (1 + spread)), NENG_unit))
        result = subprocess.run("./place_order.sh NENG USDT-PLG20 {} {} | jq '.'".format((NENG_USDT_price * (1 + spread)), NENG_unit), shell=True)
        print("./place_order.sh USDT-PLG20 NENG {} {} | jq '.'".format((USDT_NENG_price * (1 + spread)), USDT_unit))
        result = subprocess.run("./place_order.sh USDT-PLG20 NENG {} {} | jq '.'".format((USDT_NENG_price * (1 + spread)), USDT_unit), shell=True)

        print("./place_order.sh CHTA USDC-PLG20 {} {} | jq '.'".format((CHTA_USDC_price * (1 + spread)), CHTA_unit))
        result = subprocess.run("./place_order.sh CHTA USDC-PLG20 {} {} | jq '.'".format((CHTA_USDC_price * (1 + spread)), CHTA_unit), shell=True)
        print("./place_order.sh USDC-PLG20 CHTA {} {} | jq '.'".format((USDC_CHTA_price * (1 + spread)), USDC_unit))
        result = subprocess.run("./place_order.sh USDC-PLG20 CHTA {} {} | jq '.'".format((USDC_CHTA_price * (1 + spread)), USDC_unit), shell=True)

        print("./place_order.sh NENG USDC-PLG20 {} {} | jq '.'".format((NENG_USDC_price * (1 + spread)), NENG_unit))
        result = subprocess.run("./place_order.sh NENG USDC-PLG20 {} {} | jq '.'".format((NENG_USDC_price * (1 + spread)), NENG_unit), shell=True)
        print("./place_order.sh USDC-PLG20 NENG {} {} | jq '.'".format((USDC_NENG_price * (1 + spread)), USDC_unit))
        result = subprocess.run("./place_order.sh USDC-PLG20 NENG {} {} | jq '.'".format((USDC_NENG_price * (1 + spread)), USDC_unit), shell=True)
 
    ## print my MM2 recent swaps
    cur_timestamp = int(time.time())
    cutoff_time = cur_timestamp - int(args.hours * 60 * 60)
    
    with open(MM2_JSON_FILE, "r") as f:
        mm2_conf = json.load(f)
    MM2_DB_FILE = None
    path = mm2_conf["dbdir"] + "/*/MM2.db"
    for file in glob.glob(path):
        print(f"MM2.db found: {file}")
        MM2_DB_FILE = file

    dbconn = sqlite3.connect(MM2_DB_FILE)
    cursor = dbconn.cursor()
    cursor.row_factory = sqlite3.Row
    SELECT_SQL = f"SELECT stats_swaps.*, my_orders.type AS type FROM stats_swaps LEFT JOIN my_orders ON stats_swaps.uuid = my_orders.uuid WHERE started_at >= {cutoff_time} AND is_success = 1 AND (maker_coin in ('CHTA', 'NENG') or taker_coin in ('CHTA', 'NENG') )"
    print(SELECT_SQL)
    rows = cursor.execute(SELECT_SQL).fetchall()
    dbconn.close()
    ARB_DB_FILE = SCRIPT_PATH + "/arbitragedb/arb.db"
    dbconn2 = sqlite3.connect(ARB_DB_FILE)
    ## exit if another cex arbitrage trading session ongoing
    if check_cex_session(dbconn2):
        sys.exit("another cex session ongoing, exit to avoid double trades")

    ## check last 24 hours atomicDEX uuid swaps, populate swaps_arbitrage table records
    ## return true if there are newly successfully completed swaps inserted, or swaps pending for arbitrage hedging at cex
    ## exit python code if there is ongoing another job to avoid double hedging.
    is_pending_arb = check_arb_table(dbconn2,rows)
    if is_pending_arb:
        perform_arbitrage_hedge(dbconn2,cutoff_time,current_prices)
    if check_cex_session(dbconn2):
        sys.exit("trade_list cex session ongoing, exit to avoid double trades")
    else:
        perform_arbitrage_hedge_remainder(dbconn2,cutoff_time,current_prices)
        unlock_cex_session(dbconn2)   
    
def perform_arbitrage_hedge_remainder(dbconn2,cutoff_time,current_prices):
    cursor2 = dbconn2.cursor()
    cursor2.row_factory = sqlite3.Row
    SELECT_SQL = f"SELECT coin, sum(quantity) as net FROM  net_unhedged where coin = 'NENG'"
    rows = cursor2.execute(SELECT_SQL).fetchall()
    for row in rows:
        if row['coin'] is None:
            continue
        arb_price =  NENG_USDT_price  / float(current_prices["DOGE"]["last_price"])
        arb_market = 'NENG/DOGE'
        arb_side = None
        net = 0
        if (row['net'] < 0):
            arb_side = "sell"
            net = row['net'] * -1.0
        elif (row['net'] > 0):
            arb_side = "buy"
            net = row['net']
        if arb_side and (net * NENG_USDT_price > args.min_cex_usd_unit):
            print (dict(row))
            lock_cex_session(dbconn2)
            is_arb_success = run_cex_arbtrade(arb_market, arb_price, arb_side, net)
            if is_arb_success:
                hedge_side = flip_side(arb_side)
                insert_net_unhedged_record(dbconn2,'NENG', hedge_side, net);
            ## unlock_cex_session(dbconn2)
            ## exit python code to avoid double hedging.
            ## avoid bumping nonkyc.WSException Unclosed client session error, skip remainder hedge
            ## sys.exit("exit after NENG remainder cex hedging")
 
    if not check_cex_session(dbconn2):
        SELECT_SQL = f"SELECT coin, sum(quantity) as net FROM  net_unhedged where coin = 'CHTA'"
        rows = None
        rows = cursor2.execute(SELECT_SQL).fetchall()
        for row in rows:
            if row['coin'] is None:
                continue
            arb_price =  CHTA_USDT_price  / float(current_prices["DOGE"]["last_price"])
            arb_market = 'CHTA/DOGE'
            arb_side = None
            net = 0
            if (row['net'] < 0):
                arb_side = "sell"
                net = row['net'] * -1.0
            elif (row['net'] > 0):
                arb_side = "buy"
                net = row['net']
            if arb_side and (net * CHTA_USDT_price > args.min_cex_usd_unit):
                print (dict(row))
                lock_cex_session(dbconn2)
                is_arb_success = run_cex_arbtrade(arb_market, arb_price, arb_side, net)
                if is_arb_success:
                    hedge_side = flip_side(arb_side)
                    insert_net_unhedged_record(dbconn2,'CHTA', hedge_side, net);
            ##  unlock_cex_session(dbconn2)
            ## exit python code to avoid double hedging.
            ## avoid bumping nonkyc.WSException Unclosed client session error, skip remainder hedge
            ## sys.exit("exit after CHTA remainder cex hedging")
                
def perform_arbitrage_hedge(dbconn2,cutoff_time,current_prices):
    cursor2 = dbconn2.cursor()
    cursor2.row_factory = sqlite3.Row
    SELECT_SQL = f"SELECT * FROM swaps_arbitrage WHERE started_at >= {cutoff_time} AND is_success < 1"
    rows = cursor2.execute(SELECT_SQL).fetchall()
    trade_list = []
    for row in rows:
        arb_price = get_arb_price(row,current_prices)
        arb_side = None
        if (row['side'] == "buy"):
            arb_side = "sell"
        elif (row['side'] == "sell"):
            arb_side = "buy"
        if arb_side:
            if ((row['arb_market'] == 'NENG/DOGE') and (row['quantity'] * NENG_USDT_price <= args.min_cex_usd_unit)):
                insert_net_unhedged_record(dbconn2,'NENG', arb_side, row['quantity']);
                update_arb_table(dbconn2,row['uuid'], arb_price, 2)
            elif ((row['arb_market'] == 'CHTA/DOGE') and (row['quantity'] * CHTA_USDT_price <= args.min_cex_usd_unit)):
                insert_net_unhedged_record(dbconn2,'CHTA', arb_side, row['quantity']);
                update_arb_table(dbconn2,row['uuid'], arb_price, 2)
            else:
                print (dict(row))
                trade_list.append([row['uuid'], row['arb_market'], arb_price, arb_side, row['quantity']])
    
    if trade_list:
        lock_cex_session(dbconn2)
        asyncio.run(run_cex_arblist_trade(dbconn2, trade_list))
        unlock_cex_session(dbconn2)
        ## exit python code to avoid double hedging.
        ## avoid bumping nonkyc.WSException Unclosed client session error, skip remainder hedge
        sys.exit("exit after trade_list cex hedging")
            
def insert_net_unhedged_record(conn,coin, arb_side, quantity):
    if (arb_side == "sell"):
        quantity = quantity * -1.0
    
    sql = ''' INSERT INTO net_unhedged(coin,quantity)
              VALUES(?,?) '''
 
    data = (coin, quantity)
    cur = conn.cursor()
    cur.execute(sql, data)
    conn.commit()
    return cur.lastrowid

async def run_cex_arblist_trade(dbconn2, trade_list):
    config = '/opt/adex_microbot/config/nonkyc_settings.json'
    x = NonKYCClient() if not config else NonKYCClient(config)
    async with x.websocket_context() as ws:
        executed = Decimal(0)
        await x.ws_login(ws)
        for tmp_list in trade_list:
            order = None
            print(tmp_list)
            update_arb_table(dbconn2,tmp_list[0], tmp_list[2], 1)
            order = await x.ws_create_order(ws, symbol=tmp_list[1], side=tmp_list[3], quantity=str(tmp_list[4]), price=str(tmp_list[2]))
            assert (order is not None), "create order failed {}".format(tmp_list)
            assert (order['result']['id'] is not None), "create order result failed {}".format(tmp_list)
            print("create_order successfully completed order_id: {} uuid: {}".format(order['result']['id'], tmp_list[0]))
            update_arb_table(dbconn2,tmp_list[0], tmp_list[2], 2)
    await x.close()


def run_cex_arbtrade(arb_market, arb_price, arb_side, quantity):
    is_arb_success = False
    cmd = f"timeout 300 python3 {SCRIPT_PATH}/trade_nonkyc.py -t {quantity} -m {arb_market} -s {arb_side} -p {arb_price}"
    print (cmd)
    result = subprocess.run(cmd, capture_output=True, text=True, shell=True, check=False)
    print('arb CEX trade result:', result)
    m1 = re.search(
            r'create_order successfully completed', str(result), re.M)
    if m1 :
            is_arb_success = True
    
    return is_arb_success

def get_arb_price(row,current_prices):
    adex_other_coin = None 
    if 'KMD' in row['market']:
        adex_other_coin = 'KMD'
    elif 'DGB' in row['market']:
        adex_other_coin = 'DGB'
    elif 'USDT' in row['market']:
        adex_other_coin = 'USDT'
    elif 'USDC' in row['market']:
        adex_other_coin = 'USDC'
    else:
        assert True, f"Wrong market in atomicDEX {row['market']}"
    
    # CEX arb pair is always on NENG/DOGE or CHTA/DOGE at nonKYC exchange
    arb_price = row['price'] * float(current_prices[adex_other_coin]["last_price"]) / float(current_prices["DOGE"]["last_price"])
    return arb_price
    
def check_cex_session(dbconn2):
    is_cex_session_active = False
    
    cursor2 = dbconn2.cursor()
    cursor2.row_factory = sqlite3.Row
    mysql = f"SELECT * FROM cex_session"
    myarb = cursor2.execute(mysql).fetchone()
    if not myarb:
        sys.exit("Error: cex_session table emtpy")
    else:
        if myarb['lock'] == 1:
            print (f"swap ongoing, cex_session locked")
            is_cex_session_active = True

    return is_cex_session_active

def lock_cex_session(conn):
    sql = "UPDATE cex_session SET lock = 1"
    cur = conn.cursor() 
    cur.execute(sql)
    conn.commit()
    return cur.lastrowid

def unlock_cex_session(conn):
    sql = "UPDATE cex_session SET lock = 0"
    cur = conn.cursor() 
    cur.execute(sql)
    conn.commit()
    return cur.lastrowid

def check_arb_table(dbconn2, rows):
    is_pending_arb = False
    
    cursor2 = dbconn2.cursor()
    cursor2.row_factory = sqlite3.Row
    for row in rows:
        mysql = f"SELECT * FROM swaps_arbitrage WHERE uuid = '{row['uuid']}'"
        print (mysql)
        myarb = cursor2.execute(mysql).fetchone()
        if not myarb:
            print (f"... insert arb db record: uuid {row['uuid']}")
            insert_arb_record(dbconn2,row)
            is_pending_arb = True
        else:
            if myarb['is_success'] == 1:
                print (f"swap ongoing: {row['uuid']}")
                ## exit python code if there is ongoing another job to avoid double hedging.
                print("skipped to avoid double hedging {}".format({row['uuid']}))
            elif myarb['is_success'] == 2:
                print (f"swap already hedged: {row['uuid']}")
            else:
                is_pending_arb = True

    return is_pending_arb


def update_arb_table(conn,uuid, arb_price, is_success):
    sql = f"UPDATE swaps_arbitrage SET arb_price = {arb_price}, is_success = {is_success} WHERE uuid = '{uuid}'"
    print (sql)
    cur = conn.cursor() 
    cur.execute(sql)
    conn.commit()
    return cur.lastrowid


def insert_arb_record(conn,row):
    sql = ''' INSERT INTO swaps_arbitrage(market,side,quantity,price,uuid,started_at,finished_at,arb_market,arb_price,maker_pubkey,taker_pubkey )
              VALUES(?,?,?,?,?,?,?,?,?,?,?) '''
    [market, side, quantity, price] = get_market(row)
    arb_market = "unknown"
    m1 = re.search(
            r'^([NENGCHTA]+)\/\S+$', market, re.M)
    if m1 :
            arb_market = m1.group(1) + "/DOGE"
    
    arb_price = 0
    
    data = (market, side, quantity, price, row['uuid'], row['started_at'],row['finished_at'], arb_market, arb_price,row['maker_pubkey'],row['taker_pubkey'] )
    cur = conn.cursor()
    cur.execute(sql, data)
    conn.commit()
    return cur.lastrowid

def get_market(row):
    market = "unknown"
    side = "unknown"
    quantity = 0
    if row['maker_coin'] == 'NENG' or  row['maker_coin'] == 'CHTA':
        market =  row['maker_coin'] + "/" + row['taker_coin']
        side = "sell"
        quantity = row['maker_amount']
        price = row['taker_amount'] / row['maker_amount']
    elif row['taker_coin'] == 'NENG' or  row['taker_coin'] == 'CHTA':
        market =  row['taker_coin'] + "/" + row['maker_coin']
        side = "buy"
        quantity = row['taker_amount']
        price = row['maker_amount'] / row['taker_amount']

    if row['type'] == 'Taker':
        side = flip_side(side)
    return [market, side, quantity, price]

def flip_side(orderside):
    if orderside == "buy":
        orderside = "sell"
    elif orderside == "sell":
        orderside = "buy"
        
    return orderside
    
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--usd_unit', type=float, nargs='?', default=1.0 , 
                        help='USD_unit - orderbook open amount on USD worth, [default: 1.0]')
    parser.add_argument('--base_spread', nargs='?', type=float, default=0.02,
                        help='base spread in fraction from mkt price [default: 0.02]')
    parser.add_argument('--hours', nargs='?', type=float, default=24.0,
                        help='arbitrage only on past hours[default: 24.0]')
    parser.add_argument('--min_cex_usd_unit', nargs='?', type=float, default=0.0,
                        help='minimum arbitrage trading at CEX on USD worth, [default: 0.0]')
        
    args = parser.parse_args()
    # running main function
    main(args)
