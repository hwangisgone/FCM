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
		center_list.append({
			'y': round(Centroids[i][0], 2),
			'x': round(Centroids[i][1], 2),
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
from sklearn.metrics import davies_bouldin_score, silhouette_score

def calc_validations(points, labels) -> dict:
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

	return thisobj

# Actual functions to be called
def marketing_campaign(C, m, eps, max_iteration, column_array=[]) -> dict:
	filtered_df = LOADED_DF.loc[:, column_array].reset_index(drop=True).copy()
	filtered_df = filtered_df.dropna()

	print(filtered_df.head())
	print(C, m, eps, max_iteration)

	df2, centers = FCM_And_Combine(filtered_df, C=C, m=m, eps=eps, max_iteration=max_iteration)
	print(centers)

	df3 = pd.concat([filtered_df.reset_index(), df2.reset_index()], axis=1)
	df3 = df3.rename(columns={"Income": "x", "Year_Birth": "y"})

	return {
		'centroids': centers,
		'data': df3.to_dict('records'),
		'metrics': calc_validations(filtered_df, df2.idxmax(axis=1))
	}