import pandas as pd

from ..describe import describe, Description

@describe(
    Description('Correlation', 'Compute a correlation matrix for the columns of a data table.', dockerImage='analytics_tasks')
        .input('data', 'The data table', type='file', deserialize=lambda fileName: pd.read_csv(fileName, index_col=(0, 1)))
        .input('method', 'The correlation method', type='enum', values=['pearson', 'kendall', 'spearman'], default='pearson', required=False)
        .output('correlation', 'The correlation matrix between columns', type='new-file', serialize=lambda df, fileName: df.to_csv(fileName))
)
def correlation(data, method):
    return data.corr(method=method)
