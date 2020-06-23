import asyncio
import aiohttp
import logging
import json

from abc import abstractmethod
from datetime import datetime

from base import Base
from models import (
    Candlestick
)
from utils import setup_logging
from exceptions import BadResponseError

logger = setup_logging(__name__)

class Connector(Base):
    def __init__(self):
        self.session = False
        self.wss_data_count = 0

        self.logger = setup_logging(self, class_name=True, prefix_path=__name__)


    async def __aenter__(self):
        # create session on enter
        self.logger.info("Starting session")
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, *args):
        self.logger.info("Closing session")
        await self.session.close()
    
    @property
    @abstractmethod
    def api_endpoint():
        pass
    
    @property
    @abstractmethod
    def wss_endpoint():
        pass
    
    async def request(self, *a, **kw):
        response = await self._request(*a, **kw)

        if response["ok"]:
            return response["data"]

        raise BadResponseError(response["error"])


    async def _request(self, endpoint, params={}):
        """Creates HTTP request

        Args:
            endpoint (string): API endpoint
            params (dict, optional): request parameters. Defaults to {}.

        Returns:
            string: response
        """
        url = f"{self.api_endpoint}/{endpoint}"
        
        self.logger.info(f"GET request to: {url} | params: {params}")
        async with self.session.get(url, params=params) as response:
            return await self._validate_response(response)


    async def _validate_response(self, response):
        text = await response.text()

        if response.status != 200:
            self.logger.warning("Bad response")
            self.logger.warning(f"Status: {response.status}")
            self.logger.warning(f"Reason: {response.reason}")
            self.logger.warning(f"URL: {response.url}")
            self.logger.warning(f"Response: {text}")
            return self._get_error_response(response, text)

        return self._get_ok_response(response, text)

    
    def _get_ok_response(self, response, text):
        return {
            "ok": True,
            "data": json.loads(text) if text else ""
        }


    def _get_error_response(self, response, text=""):
        return {
            "ok": False,
            "error": {
                "status": response.status,
                "reason": response.reason,
                "url": response.url,
                "text": text,
            }
        }
    
    async def _wss_listen(self, url):
        """Connects to websocket stream at specified url

        Args:
            url (string): websocket url
        """
        self.logger.info(f"Connecting to websocket: {url}")
        self.wss = await self.session.ws_connect(url)
        
        while True:
            if self.wss.closed:
                self.logger.info("Connection is closed, exiting")
                break
            msg = await self.wss.receive()
            await self._handle_wss(msg)


    async def _handle_wss(self, message):
        """Handler function for different incoming frames from websocket stream

        Args:
            message (dict): message received from websocket, contains type and data
            websocket (aiohttp.client_ws.ClientWebSocketResponse): webscoket instance
        """
        msg_type = message.type
        if self.wss_data_count > 2:
            self.logger.info("Closing websocket")
            await self.wss.close()
            return

        if msg_type is aiohttp.WSMsgType.TEXT:
            self._handle_wss_data(message.data)
        elif msg_type is aiohttp.WSMsgType.PING:
            self._handle_wss_ping(message.data)
        elif msg_type is aiohttp.WSMsgType.CLOSE:
            self._handle_wss_close(message.data)
        elif msg_type is aiohttp.WSMsgType.ERROR:
            self._handle_wss_error(message.data)


    def _handle_wss_ping(self, data):
        self.logger.info("Replying to ping frame")
        self.wss.pong()

    def _handle_wss_close(self, data):
        self.logger.info("Received close frame from websocket")

    def _handle_wss_error(self, data):
        self.logger.warning(message)

    @abstractmethod
    def _handle_wss_data(self, data):
        pass
