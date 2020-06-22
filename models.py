from datetime import datetime

from sqlalchemy import Column, String, TIMESTAMP, BigInteger, Integer, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Candlestick(Base):
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
