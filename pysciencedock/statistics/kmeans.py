import pandas as pd
from sklearn.cluster import KMeans

from ..describe import describe, Description

@describe(
    Description('K means', 'Performs K means on a data table.', dockerImage='kitware/pysciencedock')
        .input('data', 'The data table', type='file', deserialize=lambda fileName: pd.read_csv(fileName, index_col=(0, 1)))
        .input('num_clusters', 'The number of clusters', type='number', min=1, step=1, default=3, required=False)
        .output('clusters', 'The data with an additional column named "cluster"', type='new-file', serialize=lambda df, fileName: df.to_csv(fileName))
        .output('cluster_centers', 'The cluster center of each cluster', type='new-file', serialize=lambda df, fileName: df.to_csv(fileName))
)
def kmeans(data, num_clusters):
    model = KMeans(n_clusters=int(num_clusters), random_state=0).fit(data)
    clusters = data.copy()
    clusters['cluster'] = model.labels_
    return dict(clusters=clusters, cluster_centers=pd.DataFrame(model.cluster_centers_, columns=data.columns))
