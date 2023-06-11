import unittest

import pandas as pd

from titanickart.processing.make_features import MakeFeatures


class TestMakeFeatures(unittest.TestCase):

    def test_make_features(self):
        data = pd.DataFrame([
            dict(Sex='male', Embarked='C'),
            dict(Sex='female', Embarked='Q'),
            dict(Sex='male', Embarked='S'),
        ])
        actual = MakeFeatures._make_features(data, use_columns=['Sex', 'Embarked_C', 'Embarked_Q', 'Embarked_S'])

        expected = pd.DataFrame([
            dict(Sex=1, Embarked_C=True, Embarked_Q=False, Embarked_S=False),
            dict(Sex=0, Embarked_C=False, Embarked_Q=True, Embarked_S=False),
            dict(Sex=1, Embarked_C=False, Embarked_Q=False, Embarked_S=True),
        ])
        pd.testing.assert_frame_equal(expected, actual.reset_index(drop=True))
