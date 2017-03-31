import pandas as pd

from hierarchy import hierarchy
from ..describe import describe, Description
from ..io import readCsv


@describe(
    Description('Heatmap', 'Compute data for a heatmap with hierarchical linkage.', dockerImage='kitware/pysciencedock')
        .input('data', 'The data table', type='file', deserialize=readCsv)
        .input('method', 'The linkage method', type='string-enumeration', values=['single', 'complete', 'average', 'weighted', 'centroid', 'median', 'ward'], default='single', required=False)
        .input('metric', 'The distance metric', type='string-enumeration', values=['euclidean', 'correlation'], default='euclidean', required=False)
        .output('matrix', 'A data table prepared for display in a heatmap', type='new-file', serialize=lambda df, fileName: df.to_csv(fileName))
)
def heatmap(data, method, metric):
    rowlinks = hierarchy(data, axis='rows', method=method, metric=metric)
    collinks = hierarchy(data, axis='columns', method=method, metric=metric)

    rowlinks['cluster'] = rowlinks.index
    rowlinks.loc[0] = [-1, -1, -1, -1, -1]
    rowlinks.columns = ['_' + c for c in rowlinks.columns]
    rowlinks.index = data.index
    data = pd.concat([data, rowlinks], axis=1)

    collinks['cluster'] = collinks.index
    for ind in range(6):
        collinks.loc[-ind] = [-1, -1, -1, -1, -1]
    collinks = collinks.transpose()
    collinks.columns = data.columns
    if len(data.index.names) > 1:
        collinks.index = [tuple(['_' + c] + ([''] * (len(data.index.names) - 1))) for c in collinks.index]
    else:
        collinks.index = ['_' + c for c in collinks.index]

    data = pd.concat([data, collinks])

    return data
