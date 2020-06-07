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



if __name__ == '__main__':
    unittest.main()
