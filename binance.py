
import logging
import json
from datetime import datetime

import engine
import database
from models import Candlestick
from utils import setup_logging, convert_timestamp
from exceptions import BadResponseError

from pprint import pprint

logger = setup_logging(__name__)


class Binance(engine.Connector):
    API_URL = "https://api.binance.com"
    WSS_URL = "wss://stream.binance.com:9443"
    API_URI = "/api/v3"
    WSS_URI = "/ws"
    
    def __init__(self):
        super().__init__()

        self.db = database.DbManager()
        self.logger = setup_logging(self, class_name=True, prefix_path=__name__)

    @property
    def api_endpoint(self):
        return f"{self.API_URL}{self.API_URI}"

    @property
    def wss_endpoint(self):
        return f"{self.WSS_URL}{self.WSS_URI}"
    
    async def _wss_listen(self, endpoint):
        # endpoint = "!miniTicker@arr"
        url = f"{self.wss_endpoint}/{endpoint}"
        await super()._wss_listen(url)

    def _handle_wss_data(self, data):
        """handles data from incoming data frames

        Args:
            data (json): incoming data from websocket stream
        """
        # self.logger.debug(json.loads(data))

        ## Steps:
        # 1. parse candlestick from data frame
        data = json.loads(data)
        c_data = data.get('k', None)

        c = Candlestick.extract_candlestick_from_wss(c_data) if c_data is not None else None
        print(f"{convert_timestamp(data.get('E'))} {c.pair} {c.interval}")

        # 2. perform TA 
        # 3. generate signals
        # 4. if candlestick is closed save to db
        if c_data.get("x", None):
            self.logger.info(f"Saving candlestick to database")
            self.db.save(c)


    async def get_server_time(self):
        """Fetches current binance server time

        Returns:
            json: dict with "serverTime" key
        """
        return await self._request("time")

    async def get_candlesticks(self, pair, limit=10, interval="15m"):
        params = {
            "symbol": pair.upper(),
            "interval": interval,
            "limit": limit
        }

        try:
            response = await self.request("klines", params=params)
        except BadResponseError as e:
            self.logger.info(e)
            return None

        objects = [Candlestick.extract_candlestick_from_api(candlestick, pair, interval) for candlestick in response]
        
        self.db.save(objects)

        return [candlestick.json for candlestick in objects]
