import numpy as np
import pandas as pd

from ..describe import describe, Description

@describe(
    Description('Normalize', 'Performs normalization of a metabolomics data table.', dockerImage='kitware/pysciencedock')
        .input('data', 'The study data table', type='file', deserialize=lambda fileName: pd.read_csv(fileName, index_col=(0, 1)))
        .input('normalization', 'Sample normalization', type='string-enumeration', values=['none', 'sum', 'median'], required=False, default='none')
        .input('transformation', 'Transformation', type='string-enumeration', values=['none', 'log', 'square root', 'cube root'], required=False, default='none')
        .input('scaling', 'Data scaling', type='string-enumeration', values=['none', 'mean', 'auto', 'pareto', 'range'], required=False, default='none')
        .output('output', 'The normalized output', type='new-file', serialize=lambda df, fileName: df.to_csv(fileName))
)
def normalize(data, normalization, scaling, transformation):
    output = data

    if normalization == 'sum':
        output = output.div(output.sum(axis=1), axis=0)
    elif normalization == 'median':
        output = output.div(output.median(axis=1), axis=0)

    if transformation == 'log':
        output = np.log10(output)
    elif transformation == 'square root':
        output = np.sqrt(output)
    elif transformation == 'cube root':
        output = np.power(output, 1.0/3.0)

    if scaling in ('mean', 'auto', 'pareto', 'range'):
        output = output.sub(output.mean(axis=0), axis=1)

    if scaling == 'auto':
        output = output.div(output.std(axis=0), axis=1)
    elif scaling == 'pareto':
        output = output.div(np.sqrt(output.std(axis=0)), axis=1)
    elif scaling == 'range':
        output = output.div(output.max(axis=0).sub(output.min(axis=0)), axis=1)

    return output
