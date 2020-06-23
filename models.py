import json

from dataclasses import dataclass, asdict
from datetime import datetime

from sqlalchemy import Column, String, TIMESTAMP, BigInteger, Integer, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ModelBase:
    def _to_json(self):
        """converts object to JSON representation

        Returns:
            [JSON]: JSON representation of object
        """
        d = asdict(self)
        
        # delete id for now
        del d["id"]
        
        # convert datetimes to timestamp
        for key, value in d.items():
            if isinstance(value, datetime):
                d[key] = int(datetime.timestamp(value))

        return json.loads(json.dumps(d))

@dataclass
class Candlestick(Base, ModelBase):
    __tablename__ = 'candlestick'

    id = Column(BigInteger, primary_key=True)
    open_time = Column(TIMESTAMP(False))
    open = Column(String)
    high = Column(String)
    low = Column(String)
    close = Column(String)
    volume = Column(String)
    close_time = Column(TIMESTAMP(False))
    quote_asset_volume = Column(String)
    trades_amount = Column(String)
    pair = Column(String)
    interval = Column(String)

    id: int
    open_time: int
    open: str
    high: str
    low: str
    close: str
    volume: str
    close_time: int
    quote_asset_volume: str
    trades_amount: str
    pair: str
    interval: str

    def __init__(
        self,
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

    ):
        self.open_time = open_time
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.close_time = close_time
        self.quote_asset_volume = quote_asset_volume
        self.trades_amount = trades_amount
        self.pair = pair
        self.interval = interval

        self.json = self._to_json()
