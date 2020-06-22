
import logging
import json
from datetime import datetime

import engine
import database
from models import Candlestick
from utils import setup_logging, convert_timestamp

logger = setup_logging(__name__)


class Binance(engine.Connector):
    API_URL = "https://api.binance.com"
    WSS_URL = "wss://stream.binance.com:9443"
    API_URI = "/api/v3"
    WSS_URI = "/ws"
    
    def __init__(self):
        super().__init__()
        # self.api_endpoint = self.api_endpoint
        # self.wss_endpoint = self.api_endpoint

        self.db = database.DbManager()
        self.logger = setup_logging(self, class_name=True, prefix_path=__name__)

    @property
    def api_endpoint(self):
        return f"{self.API_URL}{self.API_URI}"

    @property
    def wss_endpoint(self):
        return f"{self.WSS_URL}{self.WSS_URI}"
    
    async def _wss_listen(self):
        endpoint = "!miniTicker@arr"
        url = f"{WSS_URL}{WSS_URI}/{endpoint}"
        await super()._wss_listen(url)

    def _handle_wss_data(self, data):
        """handles data from incoming data frames

        Args:
            data (json): incoming data from websocket stream
        """
        self.logger.debug(json.loads(data))
        self.wss_data_count += 1

    async def get_server_time(self):
        """Fetches current binance server time

        Returns:
            json: dict with "serverTime" key
        """
        return await self._request("time")

    async def get_candlesticks(self, pair, limit=10, interval="5m"):
        params = {
            "symbol": pair.upper(),
            "interval": interval,
            "limit": limit
        }

        response = await self._request("klines", params=params)

        objects = [self._convert_response_candlestick(candlestick, pair, interval) for candlestick in json.loads(response)]
        self.db.save(objects)

        return response

    def _convert_response_candlestick(self, response, pair, interval):
        (
            open_time,
            open,
            high,
            low,
            close,
            volume,
            close_time,
            quote_asset_volume,
            trades_amount,
            *_
         ) = response

        # convert timestamps to datetime
        open_time, close_time = convert_timestamp([open_time, close_time])

        return Candlestick(
            open_time,
            open,
            high,
            low,
            close,
            volume,
            close_time,
            quote_asset_volume,
            trades_amount,
            pair,
            interval
        )
    