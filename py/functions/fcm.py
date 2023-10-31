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

import os
print(os.getcwd())

## Start entering data
df = pd.read_csv('../marketing_campaign_comma.csv')


## CLEAN UP DATA
# Add age
df['Age'] = 2023 - df.Year_Birth

# Remove deceased people
con1 = df.Age < 100
# Remove super rich CEOs
con2 = df.Income < 600000 # 600k$ / year

df = df.loc[con1 & con2]
## CLEAN UP DATA

df = df.loc[:,['Age','Income']].reset_index(drop=True)

	# Printing here
# plt.scatter(df.Age,df.Income, s=20)
# print(df.shape)
	# Printing here

# Metrics
from .cvi import dunn_fast
from sklearn.metrics import davies_bouldin_score, silhouette_score

def calc_validations(points, labels) -> dict:
	return {
		'dunn': dunn_fast(points, labels),
		'davies_bouldin': davies_bouldin_score(points, labels),
		'swc': silhouette_score(points, labels)
	}


# Actual functions to be called
def marketing_campaign(C, m, eps, max_iteration) -> dict:
	df2, centers = FCM_And_Combine(df.copy(), C=C, m=m, eps=eps, max_iteration=max_iteration)
	print(centers)

	df3 = pd.concat([df, df2], axis=1)
	df3 = df3.rename(columns={"Income": "x", "Age": "y"})

	return {
		'centroids': centers,
		'data': df3.to_dict('records'),
		'metrics': calc_validations(df, df2.idxmax(axis=1))
	}