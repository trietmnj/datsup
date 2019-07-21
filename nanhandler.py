"""
Process missing data within a dataset. 
Built on pandas DataFrame.
Requires pandas and missingno libraries.
"""
import missingno as msno
import pandas as pd
from pandas import DataFrame


def visualize(df):
	"""Plot missing cells heatmap"""
	msno.matrix(df)


def remove_rows(df: DataFrame) -> DataFrame:
	"""Removes all rows with NaN data from DataFrame"""
	return(df.dropna().reset_index(drop=True))


def remove_rows_by_col(df: DataFrame, col: str) -> DataFrame:
	"""Removes all rows with missing cells in specified column"""
	return(df[~df[col].isna()].reset_index(drop=True))


def impute(df: DataFrame, col: str, strategy: str = "zero"):
	"""
	Impute missing data in column. Random sampling hot decking.
	"""
	data = df.copy()

	if strategy == "zero":
		# works only with quant data
		filler_data = 0
	elif strategy == "mean":
		# works only with quant data
		filler_data = data[col].mean()
	elif strategy == "median":
		# works only with quant data
		filler_data = data[col].median()
	elif strategy == "most frequent":
		filler_data = data[col].mode().sample()
	elif strategy == "empty":
		filler_data = ""
	elif strategy == "hot deck":
		# replaces NaNs with random samples from valid data pool
		valid_data = data[col][~data[col].isnull()]
		sample_len = len(data[col][data[col].isnull()])
		filler_data = valid_data.sample(sample_len, replace=True).values
	else:
		raise Exception("Not a valid impute strategy")

	data[col][data[col].isnull()] = filler_data
	return(data)


def generate_binaries(df:DataFrame, cols: list):
	"""Add binary variables dependent on null vals"""
	data = df.copy()
	for col in cols:
		data[col+"_na"] = ~data[col].isnull()
	return(data)


def no_by_col(df: DataFrame):
	"""Count the number of missing data in each column"""
	return(df.isna().sum())


def replace_defects(df: DataFrame, col: str, replacement_pairs: list):
	"""Replaces """
	data = df.copy()

	for key, item in replacement_pairs.items():
		data[col] = data[col].apply(lambda x: x.replace(key, item))

	return(data)
