import numpy as np
import pandas as pd
from scipy.stats import ttest_ind

from ..describe import describe, Description
from ..io import readCsv

@describe(
    Description('T-test', 'Performs a statistical t-test on a data table.', dockerImage='kitware/pysciencedock')
        .input('data', 'The data table', type='file', deserialize=readCsv)
        .output('pvalues', 'The p-values for each column', type='new-file', serialize=lambda df, fileName: df.to_csv(fileName))
)
def ttest(data):
    if len(data.index.levels[1]) != 2:
        raise Exception('T-test requires secondary index with two values')

    indexA, indexB = data.index.levels[1]

    dataA = data.xs(indexA, level=1)
    dataB = data.xs(indexB, level=1)

    statistic, pvalues = ttest_ind(dataA, dataB)

    pvalues = pd.DataFrame(
        [statistic, pvalues, -np.log10(pvalues)],
        columns=data.columns,
        index=['t', 'p', '-log10(p)']).transpose()

    return pvalues
