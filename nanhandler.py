"""
Process missing data within a dataset. 
Built on pandas DataFrame.
Requires pandas and missingno libraries.
"""
import missingno as msno
import pandas as pd
# import support as sup
from pandas import DataFrame


def visualize(df):
	"""Plot missing cells heatmap"""
	msno.matrix(df)


def remove_rows(df: DataFrame) -> DataFrame:
	"""Removes all rows with NaN data from DataFrame"""
	return(df.dropna().reset_index().drop('index', axis=1))


def remove_rows_by_col(df: DataFrame, col: str) -> DataFrame:
	"""Removes all rows with missing cells in specified column"""
	return(df[~df[col].isna()].reset_index().drop('index', axis=1))


def impute(df: DataFrame, col: str, strategy: str = "zero"):
	"""
	Impute missing data in column. Random sampling hot decking.
	"""
	data = df.copy()

	if strategy == "zero":
		data[col][data[col].isnull()] = 0
	elif strategy == "mean":
		data[col][data[col].isnull()] = data[col].mean()
	elif strategy == "median":
		data[col][data[col].isnull()] = data[col].median()
	elif strategy == "hot deck":
		# replaces NaNs with random samples from valid data pool
		valid_data = data[col][~data[col].isnull()] 
		for i in data[col][data[col].isnull()].index:
		    data[col][i] = valid_data.sample()
	else:
		raise Exception("Not a valid impute strategy")

	return(data)


def generate_na_binaries(df:DataFrame, cols: list):
	"""Add binary variables dependent on null vals"""
	data = df.copy()
	for col in cols:
		data[col+"_na"] = ~data[col].isnull()
	return(data)


def missing_cells_by_col(df: DataFrame):
	"""Count the number of missing data in each column"""
	return(df.isna().sum())