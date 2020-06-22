
import logging
import json

import engine
from utils import setup_logging

logger = setup_logging(__name__)

API_URL = "https://api.binance.com"
WSS_URL = "wss://stream.binance.com:9443"
API_URI = "/api/v3"
WSS_URI = "/ws"

class Binance(engine.Connector):
    def __init__(self):
      super().__init__()
      self.api_endpoint = f"{API_URL}{API_URI}"
      self.wss_endpoint = f"{WSS_URL}{WSS_URI}"

      self.logger = setup_logging(self, class_name=True, prefix_path=__name__)
    
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
    