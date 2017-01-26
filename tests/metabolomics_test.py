import unittest
import pandas as pd
import numpy as np
from pandas.util.testing import assert_frame_equal
import pysciencedock.metabolomics as mb

class MetabolomicsTest(unittest.TestCase):
    def setUp(self):
        self.study = pd.DataFrame({
            'a': [1, 1],
            'b': [1, 2]
        })
        self.log = pd.DataFrame({
            'a': [0.0, 0.0],
            'b': [0.0, np.log10(2)]
        })
        self.centered = pd.DataFrame({
            'a': [0.0, 0.0],
            'b': [-0.5, 0.5]
        })
        nan = float('nan')
        std = np.std([1, 2], ddof=1)
        self.auto = pd.DataFrame({
            'a': [nan, nan],
            'b': [-0.5 / std, 0.5 / std]
        })
        self.pareto = pd.DataFrame({
            'a': [nan, nan],
            'b': [-0.5 / np.sqrt(std), 0.5 / np.sqrt(std)]
        })

    def testNormalize(self):
        output = mb.normalize(self.study)
        self.assertTrue(output.equals(self.study))

        output = mb.normalize(self.study, transformation='log')
        assert_frame_equal(output, self.log)

        output = mb.normalize(self.study, scaling='mean')
        assert_frame_equal(output, self.centered)

        output = mb.normalize(self.study, scaling='auto')
        assert_frame_equal(output, self.auto)

        output = mb.normalize(self.study, scaling='pareto')
        assert_frame_equal(output, self.pareto)
