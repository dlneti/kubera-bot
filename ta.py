import numpy as np

from typing import List, Tuple, Callable, Dict, Any

import talib

from utils import timeit

# types

Ohlcv = Dict[str, float]
TMaCallable = Callable[[np.ndarray, int], np.ndarray]

class Indicator:
    def convert_to_ndarr(self, array: List[Any]) -> np.ndarray:
        assert isinstance(array, list), "array must be a list"
        
        try:
            new_arr = np.array(array, dtype=np.float64)
        except ValueError as e:
            print(e)
            return np.array([])
        else:
            return new_arr

    def get_prices_from_ohlcv(self, prices: Ohlcv) -> np.ndarray:
        return self.convert_to_ndarr(prices["close"])

    def _filter_nan(self, arr: List[Any], filter_fn: Callable) -> List[Tuple[int, bool]]:
        return list(filter(filter_fn, arr))

    def _calculate_ma(self, ta_func: TMaCallable, timeperiod: int) -> np.ndarray:
        """calculates moving average using talib for ma

        Args:
            ta_func (function): talib function for moving average (SMA || EMA)
            timeperiod (int): timeperiod for which to calculate moving average

        Returns:
            np.ndarray: moving average
        """
        assert ta_func.__name__ in dir(talib), "ta_func must be a TA-Lib function"

        moving_average = ta_func(self.prices, timeperiod=self.long_window)

        return moving_average


class GoldenCross(Indicator):
    """
    Class representing Golden Cross indicator for both SMA and EMA
    """

    def __init__(self, prices, short_window: int, long_window: int):
        self.prices = self.get_prices_from_ohlcv(prices)
        self.short_window = short_window
        self.long_window = long_window


    def _calculate_sma(self) -> (np.ndarray, np.ndarray):
        ma_short = super()._calculate_ma(talib.SMA, self.timeperiod)
        ma_long = super()._calculate_ma(talib.SMA)
        

    def _calculate_ema(self) -> (np.ndarray, np.ndarray):
        return super()._calculate_ma(talib.EMA)


    @timeit
    def golden_cross(self, ma_short: np.ndarray, ma_long: np.ndarray) -> List[Tuple[int, bool]]:
        """Calculates golden crosses for 2 moving averages

        Args:
            ma_short (np.ndarray): short moving average
            ma_long (np.ndarray): long moving average

        Returns:
            [list]: List of tuples representing signal (1 and -1) and boolean golden cross flag (true if current signal changed from previous)
        """
        assert len(ma_short) == len(ma_long), "Moving averages length does not match!"

        index = 0
        signal_arr = []

        for i_short, i_long in zip(ma_short, ma_long):
            gc = False      # gc flag default false
            
            # start calculation from first valid pair
            if np.isnan(i_long):
                signal_arr.append((np.nan, False))
                index += 1
                continue

            if i_short > i_long:
                signal = 1
            if i_short < i_long:
                signal = -1
            
            previous_signal = signal_arr[index - 1][0]
            if previous_signal != signal and index != 0 and not np.isnan(previous_signal):
                gc = True       # signal has changed, golden cross detected at this spot

            signal_arr.append((signal, gc))
            index += 1
        
        return signal_arr
