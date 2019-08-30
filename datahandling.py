import pandas as pd
import numpy as np


def dateInRange(startDate: pd.Timestamp, endDate: pd.Timestamp):
    """Construct a generator for inclusive dates in range"""
    while startDate <= endDate:
        yield startDate
        startDate += pd.Timedelta(1, 'day')


def filterArray(tickers: np.ndarray, filterTickers: np.ndarray):
    """Filter out elements based on a filter array"""
    return np.array(
        [ticker for ticker in tickers if ticker not in filterTickers])


def combine(tickers1: np.ndarray, tickers2: np.ndarray):
    """Union string arrays"""
    return np.r_[tickers1, tickers2]


def uniqueValues(tickers: np.ndarray) -> np.ndarray:
    """Return a unique array of tickers"""
    return np.unique(tickers)
