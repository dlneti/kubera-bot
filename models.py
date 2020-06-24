import json

from dataclasses import dataclass, asdict
from datetime import datetime

from sqlalchemy import Column, String, TIMESTAMP, BigInteger, Integer, Date
from sqlalchemy.ext.declarative import declarative_base

from utils import convert_timestamp, from_sc_to_human

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

    # SQL table columns
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

    # types for dataclass
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

    def __repr__(self):
        repr_arr = [f"{from_sc_to_human(key)}: {value}" for key, value in self._to_json().items()]
        return "\n".join(repr_arr) + "\n"

    @staticmethod
    def extract_candlestick_from_api(response, pair, interval):
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

    @staticmethod
    def extract_candlestick_from_wss(data: dict) -> 'self':
        return Candlestick(
            open_time = convert_timestamp(data.get("t", None)),
            open = data.get("o", None),
            high = data.get("h", None),
            low = data.get("l", None),
            close = data.get("c", None),
            volume = data.get("v", None),
            close_time = convert_timestamp(data.get("T", None)),
            quote_asset_volume = data.get("q", None),
            trades_amount = data.get("n", None),
            pair = data.get("s", None),
            interval = data.get("i", None),
        )

# debug 
if __name__ == "__main__":
    mock_c_wss = {
    "e": "kline",     
    "E": 123456789,   
    "s": "BNBBTC",    
    "k": {
        "t": datetime.timestamp(datetime.now()), 
        "T": datetime.timestamp(datetime.now()), 
        "s": "BNBBTC",  
        "i": "1m",      
        "f": 100,       
        "L": 200,       
        "o": "0.0010",  
        "c": "0.0020",  
        "h": "0.0025",  
        "l": "0.0015",  
        "v": "1000",    
        "n": 100,       
        "x": False,
        "q": "1.0000",  
        "V": "500",     
        "Q": "0.500",   
        "B": "123456"   
    }
    } 

    mock_c_api = [
    1499040000000,        
    "0.01634790",         
    "0.80000000",         
    "0.01575800",         
    "0.01577100",         
    "148976.11427815",    
    1499644799999,        
    "2434.19055334",      
    308,                  
    "1756.87402397",      
    "28.46694368",        
    "17928899.62484339"   
    ]
    # c = Candlestick.extract_candlestick_from_api(mock_c_api, "bnbusdt", "5m")
    c = Candlestick.extract_candlestick_from_wss(mock_c_wss["k"])