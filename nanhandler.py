"""
Process missing data within a dataset. 
Requires pandas and missingno.
"""
import missingno as msno
from pandas import DataFrame


def visualize(df):
	"""Plot missing cells heatmap"""
	msno.matrix(df)


def removeRows(df: DataFrame) -> DataFrame:
	"""Removes all rows with NaN data from DataFrame"""
	return(df.dropna().reset_index(drop=True))


def removeRowsByCol(df: DataFrame, col: str) -> DataFrame:
	"""Removes all rows with missing cells in specified column"""
	return(df[~df[col].isna()].reset_index(drop=True))


def impute(df: DataFrame, col: str, strategy: str = "zero"):
	"""
	Impute missing data in column.
		df - data dataframe
		col - target column label
		strategy - imputation strategy
			zero: replaces NA with 0
			mean: replaces NA with the mean
			median: replaces NA with the median
			most frequent: replaces NA with one the mode
			empty: replaces NA with an empty str i.e. ""
			hot deck: replaces NA with a random sample of non-NA data
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
		# replaces NaNs with random samples from the valid data pool
		valid_data = data[col][~data[col].isnull()]
		sample_len = len(data[col][data[col].isnull()])
		filler_data = valid_data.sample(sample_len, replace=True).values
	else:
		raise Exception("Not a valid impute strategy")
	data[col][data[col].isnull()] = filler_data
	return(data)


def generateBinaries(df:DataFrame, cols: list):
	"""Add binary variables to specify whether obs is na"""
	data = df.copy()
	for col in cols:
		data[col+"_na"] = ~data[col].isnull()
	return(data)


def noMissingByCol(df: DataFrame):
	"""Count the number of missing data in each column"""
	return(df.isna().sum())


def replaceDefects(df: DataFrame, col: str, replacement_pairs: list):
	""" Row replacement for str based columns
		data = nan.replace_defects()
	"""
	data = df.copy()
	for key, item in replacement_pairs.items():
		data[col] = data[col].apply(lambda x: x.replace(key, item))
	return(data)
