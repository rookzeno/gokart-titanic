import unittest

import pandas as pd


class Test1(unittest.TestCase):

    def test1(self):
        pd.testing.assert_frame_equal(pd.DataFrame([]), pd.DataFrame([]))
