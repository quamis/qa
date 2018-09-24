import sys, time
import argparse
import unittest

import Tests.Base

import Solver.sum


"""
    py ./test.py -v Solver_sum_Recursive.test_4_10_1111
"""

class Solver_sum_Recursive(Tests.Base.Solver_sum_Binary):
    def getSolver(self, len, altsum, xor):
        slv = Solver.sum.Recursive()
        slv.setHint('length', len)
        slv.setHint('altsum', altsum)
        slv.setHint('xor', xor)
        return slv
        
    def getCounter(self):
        return Tests.Base.countSolver
        
    def test_4_10_1111(self):
        # 0x31313131
        self.assertEqual(self.getCounter()(self.getSolver(4, 0x00, 0x00)), 1)

if __name__ == '__main__':
    unittest.main()
    
