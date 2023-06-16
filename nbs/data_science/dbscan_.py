from __future__ import annotations

import hdbscan
import numpy as np
import pandas as pd
import plotly.express as px
import umap
from sklearn import decomposition, metrics
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler
from tqdm import tqdm

from modules.helpers import *

pd.set_option("display.max_rows", 500)
pd.set_option("display.max_columns", 500)
pd.set_option("display.width", 1000)
pd.set_option("display.float_format", "{:.3f}".format)

# Generate sample data
x, y = make_blobs(
    n_samples=10_000, centers=6, n_features=10, random_state=42, cluster_std=2.5
)

# Scale the data
x = StandardScaler().fit_transform(x)
umapper = umap.UMAP(n_components=3, n_jobs=-1, random_state=5)
x_umap = umapper.fit_transform(x)
dims = "0r 1r 2r".split()
x_umap = pd.DataFrame(x_umap, columns=dims)

pca = decomposition.PCA(random_state=5)
x_pca = pca.fit_transform(x)
x_pca = pd.DataFrame(x_pca[:, :3], columns=dims)

fig = px.scatter_3d(x_umap, *dims, color=y)
fig.update_traces(marker={"size": 3})
plot_(fig)

fig = px.scatter_3d(x_pca, *dims, color=y)
fig.update_traces(marker={"size": 3})
plot_(fig)

# Define the parameter grid
eps_range = np.arange(0.1, 1.0, 0.3)
min_samples_range = np.arange(1, 10, 3)

# params = []
# for eps in tqdm(eps_range):
#     for min_samples in min_samples_range:
#         dbscan = DBSCAN(eps=eps, min_samples=min_samples, n_jobs=-1)
#         dbscan.fit(x_pca)
#         labels = dbscan.labels_
#         score = (labels != -1).mean()
#         params.append(
#             {'eps': eps, 'min_samples': min_samples, 'score': score}
#         )
#
# params = pd.DataFrame(params)


data = []
labels = []
# Create a range of min_cluster_size values to test
min_cluster_sizes = list(range(5, 50, 5))
for min_size in tqdm(min_cluster_sizes):
    clusterer = hdbscan.HDBSCAN(min_cluster_size=min_size, core_dist_n_jobs=-1)
    clusterer.fit(x_pca[dims])
    n_cluster = len(np.unique(clusterer.labels_))
    silhouette_score = metrics.silhouette_score(x_pca, clusterer.labels_)
    data.append([min_size, n_cluster, silhouette_score])
    x_pca[f"hdbscan_{min_size}"] = clusterer.labels_

    clusterer = hdbscan.HDBSCAN(min_cluster_size=min_size, core_dist_n_jobs=-1)
    clusterer.fit(x_umap[dims])
    x_umap[f"hdbscan_{min_size}"] = clusterer.labels_

df = pd.DataFrame(
    data, columns=["min_size", "n_cluster", "silhouette_score"]
).sort_values("silhouette_score")

for i in min_cluster_sizes[::2]:
    fig = px.scatter_3d(x_umap, *dims, color=f"hdbscan_{i}")
    fig.update_traces(marker={"size": 3})
    plot_(fig)
