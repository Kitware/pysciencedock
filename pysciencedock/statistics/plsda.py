import pandas as pd
from sklearn.cross_decomposition import PLSRegression

from ..describe import describe, Description

@describe(
    Description('Normalize', 'Performs partial least squares descriminant analysis on a data table.', dockerImage='analytics_tasks')
        .input('data', 'The data table', type='file', deserialize=lambda fileName: pd.read_csv(fileName, index_col=(0, 1)))
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
