import pandas as pd
import numpy as np

def ss_calc_centroids(df, U_s, U, C, m):
	Centroids = np.zeros((C, df.shape[1]))
	
	for i in range (C):
		temp = abs(U[:,i] - U_s[:,i])**m;	# Might need revision
		Centroids[i, :] = np.sum((temp)[:,np.newaxis]*df, axis=0)/np.sum(temp)
	return Centroids
# [x1, y1], [x2, y2]
# Where 1 is cluster 1
# df: dataframe with x and y
# C: number of cluster
# U: Randomized data value for each cluster for each point
# m: m

def ss_calc_new_membership(df, U_s, Centroids, C, m):
	Distance = np.zeros((df.shape[0], C))
	for i in range (C):
		Distance[:, i] = np.linalg.norm(df - Centroids[i, :], axis=1)

	
	U_new = 1/ (Distance ** (2/(m-1)) * np.sum((1/Distance) ** (2/(m-1)), axis=1)[:, np.newaxis])
	U_new_s = U_s + (1 - np.sum(U_s , axis=1)[:, np.newaxis])*U_new
	return U_new_s


# Variables needed: 
# df: original df with 2 columns
# U_s: np array of supervised members. Can be zero if not initialized.
# C: number of cluster
# m: fuzzy partition matrix exponent
# eps: error level (stop if the change is <= than this)
# max_iteration
def ss_FCM_And_Combine(df, U_s, C, m, eps, max_iteration):
	U = np.random.rand(df.shape[0], C)
	
	for iteration in range (max_iteration):
		Centroids = ss_calc_centroids(df, U_s, U, C, m)
		U_new = ss_calc_new_membership(df, U_s, Centroids, C, m)

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