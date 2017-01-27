import numpy as np
import pandas as pd

from ..describe import describe, Description

@describe(
    Description('Fold change', 'Perform a fold change analysis.', dockerImage='kitware/pysciencedock')
        .input('data', 'The input data table', type='file', deserialize=lambda fileName: pd.read_csv(fileName, index_col=(0, 1)))
        .input('threshold', 'Fold change threshold', type='number', min=0, default=2, required=False)
        .output('output', 'The fold change table', type='new-file', serialize=lambda df, fileName: df.to_csv(fileName))
)
def foldchange(data, threshold):
    if len(data.index.levels[1]) != 2:
        raise Exception('Fold change requires secondary index with two values')

    indexA, indexB = data.index.levels[1]

    meanA = data.xs(indexA, level=1).mean(axis=0)
    meanB = data.xs(indexB, level=1).mean(axis=0)

    change = meanB.div(meanA)

    output = pd.DataFrame([change, np.log2(change)], ['Fold change', 'Log2 fold change']).transpose()
    if threshold > 0:
        output = output.select(lambda x: output['Fold change'][x] > threshold or output['Fold change'][x] < 1/threshold)
    return output.sort_values(by='Fold change', ascending=False)
