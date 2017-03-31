import pandas as pd

from ..describe import describe, Description
from ..io import readCsv

@describe(
    Description('Concatenate', 'Concatenates two data tables.', dockerImage='kitware/pysciencedock')
        .input('table1', 'The first data table', type='file', deserialize=readCsv)
        .input('table2', 'The second data table', type='file', deserialize=readCsv)
        .output('combined', 'The combined table', type='new-file', serialize=lambda df, fileName: df.to_csv(fileName))
)
def concatenate(table1, table2):
    return pd.concat([table1, table2])
