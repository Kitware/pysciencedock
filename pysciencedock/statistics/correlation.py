import pandas as pd

from ..describe import describe, Description
from ..io import readCsv

@describe(
    Description('Correlation', 'Compute a correlation matrix for the columns of a data table.', dockerImage='kitware/pysciencedock')
        .input('data', 'The data table', type='file', deserialize=readCsv)
        .input('method', 'The correlation method', type='string-enumeration', values=['pearson', 'kendall', 'spearman'], default='pearson', required=False)
        .output('correlation', 'The correlation matrix between columns', type='new-file', serialize=lambda df, fileName: df.to_csv(fileName))
)
def correlation(data, method):
    return data.corr(method=method)
