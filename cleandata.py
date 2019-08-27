"""General data manipulation"""
from pandas import DataFrame


def replaceChar(df: DataFrame, colName: str, keyPairs: dict):
    """Replaces char in string based columns"""
    for key, value in keyPairs.items():
        df[colName] = df[colName].map(lambda x: x.replace(key, value))
