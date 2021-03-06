import asyncio
import logging
import json

import binance
from utils import setup_logging

# create logger
logger = setup_logging(initial=True)

async def main(loop):
    async with binance.Binance() as client:
        # response = await client.get_candlesticks("BTCUSDT")
        # print(response)
        await client._wss_listen("ethusdt@kline_1m")
        


loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))