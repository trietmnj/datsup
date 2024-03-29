'''Raw data manipulation. Included tools aim to turn dataset "tidy"'''
import pandas as pd
from pandas import DataFrame
from typing import List


def flagDefaultIndex(df:DataFrame) -> bool:
    '''Check whether DataFrame has a default index'''
    return type(df.index) == pd.RangeIndex


def melt(df:DataFrame, id_var_list:list, var_name:str, value_name:str) -> DataFrame:
    '''Unpivot DataFrame to long format. Reset indexing as applicable'''
    data = df.copy()
    if not flagDefaultIndex(df):
        idx_name = df.index.name
        data = df.reset_index()
        id_var_list.insert(0, idx_name)
    return data.melt(id_vars=id_var_list, var_name=var_name, value_name=value_name)

# TODO, rewrite for OOP
