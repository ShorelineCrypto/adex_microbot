#!/usr/bin/env python3
from nonkyc import NonKYCClient
import argparse
from decimal import Decimal
import asyncio, signal

async def ioc(args):
    x = NonKYCClient() if not args.config else NonKYCClient(args.config)
    result = None
    async with x.websocket_context() as ws:
        executed = Decimal(0)
        await x.ws_login(ws)
        order = await x.ws_create_order(ws, symbol=args.market, side=args.side, quantity=str(args.total), price=str(args.price))
      ## immediately cancel newly opened order
      ## ord_cancelled = await x.ws_cancel_order(ws, order['result']['id'])
      ##  executed = Decimal(ord_cancelled['result']['executedQuantity'])
      
      ## immediately execute order, may wait > 3 minutes, may stuck there in log
      ##  executed = Decimal(order['result']['executedQuantity'])
      ##  symbol = args.market.split('/') if '/' in args.market else args.market.split('_')
      ##  print(f"Executed: {executed}{symbol[0]}")
        await asyncio.sleep(2)
        assert (order['result']['id'] is not None), "create order failed"
        print("create_order successfully completed order_id: {}".format(order['result']['id']))
        result = "create_order successfully completed order_id: {}".format(order['result']['id'])
    await x.close()
    return result

if __name__ == '__main__':
    args = argparse.ArgumentParser(description='Creates An order at a specific price and cancels it immediately. Returns the amount that was executed.')
    args.add_argument('-c', '--config', action = 'store', required=False, default='/opt/adex_microbot/config/nonkyc_settings.json',
                      help="path to a json file with your api keys. default '/opt/adex_microbot/config/nonkyc_settings.json', See"\
                      "NonKYCPythonClient README.md")
    args.add_argument('-t', '--total', action='store', required = True,
                      help="Total amount to be traded")
    args.add_argument('-m', '--market', action='store', required = True,
                      help="Market symbol, eg. NENG/DOGE")
    args.add_argument('-s', '--side', action='store', choices=['buy','sell'],
                      help="My trade side (buy or sell)")
    args.add_argument('-p', '--price', action='store', required=True, type=Decimal,
                      help="Price of the IOC order")
    arguments = args.parse_args()
    print(arguments)
    result = asyncio.run(ioc(arguments))
    print(result)

