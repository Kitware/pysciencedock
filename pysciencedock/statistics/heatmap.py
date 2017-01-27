import pandas as pd

from hierarchy import hierarchy
from ..describe import describe, Description

@describe(
    Description('Heatmap', 'Compute data for a heatmap with optional hierarchical linkage.', dockerImage='kitware/pysciencedock')
        .input('data', 'The data table', type='file', deserialize=lambda fileName: pd.read_csv(fileName, index_col=(0, 1)))
        .input('method', 'The linkage method', type='enum', values=['single', 'complete', 'average', 'weighted', 'centroid', 'median', 'ward'], default='single', required=False)
        .input('metric', 'The distance metric', type='enum', values=['euclidean', 'correlation'], default='euclidean', required=False)
        .output('rowlinks', 'The linkage tree of rows', type='new-file', serialize=lambda df, fileName: df.to_csv(fileName))
        .output('collinks', 'The linkage tree of columns', type='new-file', serialize=lambda df, fileName: df.to_csv(fileName))
        .output('matrix', 'The original data for display in the heatmap', type='new-file', serialize=lambda df, fileName: df.to_csv(fileName))
)
def heatmap(data, method, metric):
    rowlinks = hierarchy(data, axis='rows', method=method, metric=metric)
    collinks = hierarchy(data, axis='columns', method=method, metric=metric)

    return dict(
        matrix=data,
        rowlinks=rowlinks,
        collinks=collinks)
