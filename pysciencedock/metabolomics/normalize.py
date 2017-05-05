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
        output = output / output.sum()
    elif normalization == 'median':
        output = output / output.median()

    if transformation == 'log':
        output = np.log10(output)
    elif transformation == 'square root':
        output = np.sqrt(output)
    elif transformation == 'cube root':
        output = np.power(output, 1.0/3.0)

    if scaling in ('mean', 'auto', 'pareto', 'range'):
        output = output - output.mean()

    if scaling == 'auto':
        output = output / output.std()
    elif scaling == 'pareto':
        output = output / np.sqrt(output.std())
    elif scaling == 'range':
        output = output / (output.max() - output.min())

    return output
