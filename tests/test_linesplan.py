#!/usr/bin/env python

from testing_utils import *

from hydros.linesplan import *

import difflib

class TestLinesPlan(unittest.TestCase):
    pass


class TestFunctions(unittest.TestCase):

    def test_load_save(self):
        f1 = 'data/fcs_3307.json'
        f2 = 'output/fcs_3307.json'
        lines = load_lines_plan(f1)
        save_lines_plan(lines, f2)
        with open(f1) as f:
            s1 = f.readlines()
        with open(f2) as f:
            s2 = f.readlines()
        diffs = list(difflib.unified_diff(s1, s2))
        self.assertFalse(diffs)

    def test_get_waterline_properties(self):
        w1 = [[1.0, 0.0, 2.0], [1.0, 1.0, 2.0], [2.0, 2.0, 2.0], [2.0, 0.0, 2.0]]
        w2 = [[-2.0, 0.0, 2.0], [-2.0, 2.0, 2.0], [-1.0, 1.0, 2.0], [-1.0, 0.0, 2.0]]
        a1, m1x, m1x2, m1y, m1y2 = get_waterline_properties(w1)
        a2, m2x, m2x2, m2y, m2y2 = get_waterline_properties(w2)
        self.assertEqual(a1, a2)
        self.assertEqual(m1x, m2x)
        self.assertEqual(m1x, 7.0 / 6.0)
        self.assertEqual(m1y, -m2y)
        self.assertEqual(m1y, 7.0 / 3.0)
        self.assertEqual(m1x2, m2x2)
        self.assertEqual(m1x2, 5.0 / 4.0)
        self.assertEqual(m1y2, m2y2)
        self.assertEqual(m1y2, 15.0 / 4.0) 



if __name__ == '__main__':
    unittest.main()
