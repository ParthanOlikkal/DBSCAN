import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
%matplotlib inline

#Data generation
#The function below generates the data points and requires centroidLocation, numSamples and  clusterDeviation as inputs
def createDataPoints(centroidLocation, numSamples, clusterDeviation):
	#Create random data and store in feature matrix x and response vector y
	X, y = make_blobs(n_samples=numSamples, centers=centroidLocation, cluster_std=clusterDeviation)
	
	#Standardize features by removing mean and scaling to unit variance
	X = StandardScaler().fit_transform(X)
	return X, y

X, y = createDataPoints([[4,3], [2,-1], [-1,4]], 1500, 0.5)

#Modeling
#Here epsilon means radius of the neighborhood

epsilon = 0.3
minimumSamples = 7
db = DBSCAN(eps=epsilon, min_samples=minimumSamples).fit(X)
labels = db.labels_
labels

#Distinguish Outliers by replacing all elements with true in core_samples that are in the cluster and false if the points are outliers
#First create an array of booleans using the labels from db
core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
core_samples_mask[db.core_sample_indices_] = True
core_samples_mask

#Number of clusters in labels, ignoring noise if present
n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
n_clusters_

#Remove repetition in labels by turning it into a set
unique_labels = set(labels)
unique_labels

#Data Visualization
#Create colors for the clusters
colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
colors

#Plot the points with colors
for k, col in zip(unique_labels, colors):
	if k == -1:
		#Black used for noise
		col = 'k'
	class_member_mask = (labels == k)

#Plot the datapoints that are clustered
xy = X[class_member_mask & core_samples_mask]
plt.scatter(xy[:, 0], xy[:, 1], s=50, c=col, marker=u'o', alpha=0.5)

#Plot the outliers
xy = X[class_member_mask & ~core_samples_mask]
plt.scatter(xy[:, 0], xy[:, 1], s=50, c=col, marker=u'o', alpha=0.5)
