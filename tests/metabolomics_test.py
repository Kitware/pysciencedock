import unittest
import pandas as pd
import numpy as np
from pandas.util.testing import assert_frame_equal
import pysciencedock.metabolomics as mb

class MetabolomicsTest(unittest.TestCase):
    def setUp(self):
        self.study = pd.DataFrame({
            'a': [1, 2, 3],
            'b': [2, 4, 6],
            'c': [3, 6, 9]
        })
        self.median = pd.DataFrame({
            'a': [0.5, 1, 1.5],
            'b': [0.5, 1, 1.5],
            'c': [0.5, 1, 1.5]
        })
        self.sum = pd.DataFrame({
            'a': [1/6.0, 2/6.0, 0.5],
            'b': [1/6.0, 2/6.0, 0.5],
            'c': [1/6.0, 2/6.0, 0.5]
        })
        self.log = pd.DataFrame({
            'a': [0.0, np.log10(2), np.log10(3)],
            'b': [np.log10(2), np.log10(4), np.log10(6)],
            'c': [np.log10(3), np.log10(6), np.log10(9)]
        })
        self.sqrt = pd.DataFrame({
            'a': [1, np.sqrt(2), np.sqrt(3)],
            'b': [np.sqrt(2), np.sqrt(4), np.sqrt(6)],
            'c': [np.sqrt(3), np.sqrt(6), np.sqrt(9)]
        })
        self.cbrt = pd.DataFrame({
            'a': [1, np.power(2, 1.0/3.0), np.power(3, 1.0/3.0)],
            'b': [np.power(2, 1.0/3.0), np.power(4, 1.0/3.0), np.power(6, 1.0/3.0)],
            'c': [np.power(3, 1.0/3.0), np.power(6, 1.0/3.0), np.power(9, 1.0/3.0)]
        })
        self.centered = pd.DataFrame({
            'a': [-1.0, 0.0, 1.0],
            'b': [-2.0, 0.0, 2.0],
            'c': [-3.0, 0.0, 3.0]
        })
        self.auto = pd.DataFrame({
            'a': [-1.0, 0.0, 1.0],
            'b': [-1.0, 0.0, 1.0],
            'c': [-1.0, 0.0, 1.0]
        })
        self.pareto = pd.DataFrame({
            'a': [-1.0, 0.0, 1.0],
            'b': [-np.sqrt(2), 0.0, np.sqrt(2)],
            'c': [-np.sqrt(3), 0.0, np.sqrt(3)]
        })
        self.range = pd.DataFrame({
            'a': [-0.5, 0.0, 0.5],
            'b': [-0.5, 0.0, 0.5],
            'c': [-0.5, 0.0, 0.5]
        })


    def testNormalize(self):
        output = mb.normalize(self.study, normalization='median')
        assert_frame_equal(output, self.median)

        output = mb.normalize(self.study, normalization='sum')
        assert_frame_equal(output, self.sum)

        output = mb.normalize(self.study, transformation='log')
        assert_frame_equal(output, self.log)

        output = mb.normalize(self.study, transformation='square root')
        assert_frame_equal(output, self.sqrt)

        output = mb.normalize(self.study, transformation='cube root')
        assert_frame_equal(output, self.cbrt)

        output = mb.normalize(self.study, scaling='mean')
        assert_frame_equal(output, self.centered)

        output = mb.normalize(self.study, scaling='auto')
        assert_frame_equal(output, self.auto)

        output = mb.normalize(self.study, scaling='pareto')
        assert_frame_equal(output, self.pareto)

        output = mb.normalize(self.study, scaling='range')
        assert_frame_equal(output, self.range)
