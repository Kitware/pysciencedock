import pandas as pd

from ..describe import describe, Description
from ..io import readCsv

@describe(
    Description('CSV to JSON', 'Converts a CSV table to an array of objects in JSON format.', dockerImage='kitware/pysciencedock')
        .input('data', 'The CSV data table', type='file', deserialize=readCsv)
        .output('output', 'The converted JSON table', type='new-file', serialize=lambda df, fileName: df.to_json(fileName))
)
def csv_to_json(data):
    return data
