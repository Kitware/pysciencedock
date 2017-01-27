import numpy as np
import pandas as pd
from sklearn.decomposition import PCA

from ..describe import describe, Description

@describe(
    Description('PCA', 'Performs principal component analysis of a data table.', dockerImage='kitware/pysciencedock')
        .input('data', 'The data table', type='file', deserialize=lambda fileName: pd.read_csv(fileName, index_col=(0, 1)))
        .input('num_components', 'The number of components', type='number', min=1, step=1, default=5, required=False)
        .output('explained', 'The explained variance for each component', type='new-file', serialize=lambda df, fileName: df.to_csv(fileName))
        .output('components', 'The component vectors', type='new-file', serialize=lambda df, fileName: df.to_csv(fileName))
)
def pca(data, num_components):
    pcaModel = PCA(n_components=int(num_components))
    pcaModel.fit(data.transpose())
    explained = pd.Series(pcaModel.explained_variance_ratio_)
    components = pd.DataFrame(pcaModel.components_.transpose(), index=data.index)
    return dict(explained=explained, components=components)
