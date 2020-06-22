import asyncio
import logging
import json

import binance
from utils import setup_logging

# create logger
logger = setup_logging(initial=True)

async def main(loop):
    async with binance.Binance() as client:
        response = await client.get_candlesticks("ETHUSDT")
        # await client._wss_listen()


loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))