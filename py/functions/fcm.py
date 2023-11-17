import pandas as pd
import numpy as np

def calc_centroids(df, U, C, m):
	Centroids = np.zeros((C, df.shape[1]))
	
	for i in range (C):
		Centroids[i, :] = np.sum((U[:,i]**m)[:,np.newaxis]*df, axis=0)/np.sum(U[:,i]**m)
	return Centroids
# [x1, y1], [x2, y2]
# Where 1 is cluster 1
# df: dataframe with x and y
# C: number of cluster
# U: Randomized data value for each cluster for each point
# m: m

def calc_new_membership(df, Centroids, C, m):
	Distance = np.zeros((df.shape[0], C))
	for i in range (C):
		Distance[:, i] = np.linalg.norm(df - Centroids[i, :], axis=1)

	U_new = 1/ (Distance ** (2/(m-1)) * np.sum((1/Distance) ** (2/(m-1)), axis=1)[:, np.newaxis])
	return U_new


# Variables needed: 
# df: original df with 2 columns
# C: number of cluster
# m: fuzzy partition matrix exponent
# eps: error level (stop if the change is <= than this)
# max_iteration
def FCM_And_Combine(df, C, m, eps, max_iteration):
	U = np.random.rand(df.shape[0], C)
	
	for iteration in range (max_iteration):
		Centroids = calc_centroids(df, U, C, m)
		U_new = calc_new_membership(df, Centroids, C, m)

		if np.linalg.norm(U_new - U) <= eps:
			print("Final:\n")
			break

		U = U_new
		
	column_names = []
	center_list = []
	for i in range(0, U.shape[1]):
		clustername = f'Cluster {i+1}'
		column_names.append(clustername)
		print(clustername, Centroids[i])

		center_list.append({
			'centroids': Centroids[i],
			'name': clustername
		})

	return pd.DataFrame(U, columns=column_names), center_list

##################################
## Functions to be used outside ##
##################################
import os
print(os.getcwd())

## Load tkinter
import tkinter
from tkinter import filedialog as fd

## Create empty dataframe
LOADED_DF = pd.DataFrame()
RESULT_DF = pd.DataFrame()

def load_data_csv() -> list:
	tkinter.Tk().withdraw()
	root = tkinter.Tk()
	root.attributes("-alpha", 0.0)
	root.attributes("-topmost", True)

	columns = []
	file = fd.askopenfile(mode='r', parent=root, title="Choose a file", filetypes=[('CSV Files', '*.csv')])
	if file:
		global LOADED_DF
		LOADED_DF = pd.read_csv(file)
		print(LOADED_DF.head())
		columns = list(LOADED_DF.columns)

	root.destroy()
	return columns


	# ## CLEAN UP DATA
	# # Add age
	# df['Age'] = 2023 - df.Year_Birth

	# # Remove deceased people
	# con1 = df.Age < 100
	# # Remove super rich CEOs
	# con2 = df.Income < 600000 # 600k$ / year

	# df = df.loc[con1 & con2]
	# ## CLEAN UP DATA



		# Printing here
	# plt.scatter(df.Age,df.Income, s=20)
	# print(df.shape)
		# Printing here

# Metrics
from .cvi import dunn_fast
from sklearn.metrics import davies_bouldin_score, silhouette_score, rand_score, adjusted_rand_score

def calc_external_validations(targets, predictions) -> dict:
	return {
		'rand': {
			'name': "Rand index",
			'result': rand_score(targets, predictions),
			'mindiff': 0.0001
		},
		'adjrand': {
			'name': "Adjusted Rand index (ARI)",
			'result': adjusted_rand_score(targets, predictions),
			'mindiff': 0.0001
		}
	}

def calc_relative_validations(points, labels) -> dict:
	return {
		'dunn': {
			'name': "Dunn's index",
			'result': dunn_fast(points, labels),
			'mindiff': 0.0001
		},
		'davies_bouldin': {
			'name': "Davies-Bouldin index",
			'result': davies_bouldin_score(points, labels),
			'mindiff': -0.01
		},
		'swc': {
			'name': "Silhouette width criterion (SWC)",
			'result': silhouette_score(points, labels),
			'mindiff': 0.0001
		}
	}

# Actual functions to be called
def marketing_campaign(C, m, eps, max_iteration, column_array=[], column_labeled="") -> dict:
	filtered_df = LOADED_DF.loc[:, column_array].reset_index(drop=True).copy()
	filtered_df = filtered_df.dropna()

	print(filtered_df.head())
	print(C, m, eps, max_iteration)

	# Save as global to display later
	result_df2, centers_list = FCM_And_Combine(filtered_df, C=C, m=m, eps=eps, max_iteration=max_iteration)

	# Fix center naming
	for center in centers_list:
		for idx, col in enumerate(column_array):
			center[col] = center['centroids'][idx]
		del center['centroids']

	# Concat to one giant data
	df3 = pd.concat([filtered_df.reset_index(drop=True), result_df2.reset_index(drop=True)], axis=1)
	print(df3.head())

	datadict = {
		'centroids': centers_list,
		'data': df3.to_dict('records'),
		'metrics': calc_relative_validations(filtered_df, result_df2.idxmax(axis=1)) # Chosing one label for each point based on the highest value
	}

	if column_labeled != "":
		# Rename target and prediction columns to numbers
		preds = pd.factorize(result_df2.idxmax(axis=1))[0]		# Return codes: nparray, uniques: nparray
		targets = pd.factorize(LOADED_DF.dropna(subset=column_array)[column_labeled])[0]	# Return codes: nparray, uniques: nparray

		datadict['metrics'].update(calc_external_validations(targets, preds))

	return datadict
		