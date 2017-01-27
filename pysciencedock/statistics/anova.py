import numpy as np
import pandas as pd
from scipy.stats import f_oneway

from ..describe import describe, Description

@describe(
    Description('ANOVA', 'Performs a one-way analysis of variance test on a data table.', dockerImage='kitware/pysciencedock')
        .input('data', 'The data table', type='file', deserialize=lambda fileName: pd.read_csv(fileName, index_col=(0, 1)))
        .output('pvalues', 'The p-values for each column', type='new-file', serialize=lambda df, fileName: df.to_csv(fileName))
)
def anova(data):
    if len(data.groupby(level=1)) <= 2:
        raise Exception('ANOVA requires a secondary index with three or more values')

    return pd.DataFrame(
        [f_oneway(*[v for k, v in data[col].groupby(level=1)]) for col in data.columns],
        columns=['f', 'p'],
        index=data.columns)
