import pandas as pd
from scipy.cluster.hierarchy import linkage

from ..describe import describe, Description

@describe(
    Description('Hierarchical linkage', 'Compute a hierarchical linkage of the rows or columns of a data table.', dockerImage='kitware/pysciencedock')
        .input('data', 'The data table', type='file', deserialize=lambda fileName: pd.read_csv(fileName, index_col=(0, 1)))
        .input('axis', 'Observations are stored in', type='enum', values=['rows', 'columns'], default='rows', required=False)
        .input('method', 'The linkage method', type='enum', values=['single', 'complete', 'average', 'weighted', 'centroid', 'median', 'ward'], default='single', required=False)
        .input('metric', 'The distance metric', type='enum', values=['euclidean', 'correlation'], default='euclidean', required=False)
        .output('linkage', 'The linkage tree', type='new-file', serialize=lambda df, fileName: df.to_csv(fileName))
)
def hierarchy(data, axis, method, metric):
    if axis == 'columns':
        data = data.transpose()
    clusters = range(len(data.index), 2*len(data.index) - 1)
    result = pd.DataFrame(
        linkage(data, method=method, metric=metric),
        columns=['child1', 'child2', 'distance', 'size'],
        index=clusters)
    for col in ['child1', 'child2', 'size']:
        result[col] = result[col].astype(int)
    return result
