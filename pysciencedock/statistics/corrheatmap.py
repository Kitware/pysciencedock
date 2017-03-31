import pandas as pd

from ..describe import describe, Description
from ..io import readCsv
from heatmap import heatmap

@describe(
    Description('Correlation Heatmap', 'Compute a correlation matrix for the columns of a data table with hierarchical linkage.', dockerImage='kitware/pysciencedock')
        .input('data', 'The data table', type='file', deserialize=readCsv)
        .input('method', 'The correlation method', type='string-enumeration', values=['pearson', 'kendall', 'spearman'], default='pearson', required=False)
        .input('linkage', 'The linkage method', type='string-enumeration', values=['single', 'complete', 'average', 'weighted', 'centroid', 'median', 'ward'], default='single', required=False)
        .output('correlation', 'The correlation matrix between columns', type='new-file', serialize=lambda df, fileName: df.to_csv(fileName))
)
def corrheatmap(data, method, linkage):
    corr = data.corr(method=method)
    heat = heatmap(corr, method=linkage, metric='correlation')

    # Put optional secondary index in _class column.
    if len(data.index.names) > 1:
        data['_class'] = data.index.get_level_values(data.index.names[1])
        data.index = data.index.get_level_values(data.index.names[0])

    return pd.concat([heat, data])
