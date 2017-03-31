import pandas as pd
from sklearn.cross_decomposition import PLSRegression

from ..describe import describe, Description
from ..io import readCsv

@describe(
    Description('PLSDA', 'Performs partial least squares descriminant analysis on a data table.', dockerImage='kitware/pysciencedock')
        .input('data', 'The data table', type='file', deserialize=readCsv)
        .input('num_components', 'The number of components', type='number', min=1, step=1, default=5, required=False)
        .output('loadings', 'The loadings', type='new-file', serialize=lambda df, fileName: df.to_csv(fileName))
        .output('scores', 'The scores', type='new-file', serialize=lambda df, fileName: df.to_csv(fileName))
)
def plsda(data, num_components):
    plsModel = PLSRegression(n_components=int(num_components))
    plsModel.fit(data, data.index.labels[1])
    loadings = pd.DataFrame(plsModel.x_loadings_, index=data.columns)
    scores = pd.DataFrame(plsModel.x_scores_, index=data.index)
    return dict(loadings=loadings, scores=scores)
