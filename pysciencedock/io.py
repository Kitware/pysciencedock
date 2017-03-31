import pandas as pd
import six

def readCsv(fileName):
    data = pd.read_csv(fileName, nrows=1)
    indexCol = []
    for col in range(len(data.columns)):
        colName = data.columns[col]
        if colName.startswith('Unnamed') or colName.startswith('_') or isinstance(data.iloc[0, col], six.string_types):
            indexCol.append(col)
        else:
            break
    data = pd.read_csv(fileName, index_col=indexCol)

    def transformName(name):
        if name is None or name.startswith('_'):
            return name
        return '_' + name

    data.index.names = [transformName(name) for name in data.index.names]
    return data
