import sys, time
import argparse
import unittest

import Tests.Base

import Solver.sum
import Solver.sumAndMedian
import Solver.sumAndMD5


"""
    py ./test.py -v Solver_sum_RecursiveOptimized_withInterval.test_06_10_rrnmeeeaaa
    py ./test.py -v Solver_sum_RecursiveOptimized_withInterval.test_16_10_srrrpnmieeeeeaaa
    
    py ./test.py -v Solver_sum_RecursiveOptimized_withInterval_withMedian_V1.test_06_10_rrnmeeeaaa
    
    py ./test.py -v Solver_sum_RecursiveOptimized_withInterval_withMedian_Optimized.test_06_10_rrnmeeeaaa

"""

class Solver_sum_Recursive(Tests.Base.Solver_sum_Binary):
    def getSolver(self, len, sum):
        slv = Solver.sum.Recursive()
        slv.setHint('length', len)
        slv.setHint('sum', sum)
        return slv
        
    def getCounter(self):
        return Tests.Base.countSolver
  

class Solver_sum_RecursiveOptimized(Tests.Base.Solver_sum_Binary_withCallback):
    def getSolver(self, len, sum):
        slv = Solver.sum.RecursiveOptimized()
        slv.setHint('length', len)
        slv.setHint('sum', sum)
        return slv
        
    def getCounter(self):
        return Tests.Base.countSolverWithCallback
    
    def test_6_z_0x01(self):
        self.assertEqual(self.getCounter()(self.getSolver(6, 0x01)), 1)
        
    def test_6_z_0x02(self):
        self.assertEqual(self.getCounter()(self.getSolver(6, 0x02)), 2)
        
    def test_6_z_0x06(self):
        self.assertEqual(self.getCounter()(self.getSolver(6, 0x06)), 11)
     
    # way too slow
    #def test_6_s_623(self):
    #    self.assertEqual(self.getCounter()(self.getSolver(6, 623)), 11)
        
        
        
        
class Solver_sum_RecursiveOptimized_withInterval(Tests.Base.Solver_sum_Words_withCallback):
    def getSolver(self, len, sum, interval):
        slv = Solver.sum.RecursiveOptimized()
        
        # min width: 4+4+2 = 10
        slv.setHint('length', len)
        slv.setHint('sum', sum)
        slv.setHint('interval', (max(interval), min(interval)))
        return slv
        
    def test_02_10_ba(self):
        self.assertEqual(self.getHitCounter()('ba'.encode('utf-8'), self.getSolver(2, 195, (0x62, 0x61))), 1)
        
    def test_02_11_za(self):
        self.assertEqual(self.getHitCounter()('za'.encode('utf-8'), self.getSolver(2, 219, (0x7a, 0x61))), 1)
        
    def test_04_10_cbaa(self):
        self.assertEqual(self.getHitCounter()('cbaa'.encode('utf-8'), self.getSolver(4, 391, (0x63, 0x61))), 1)
        
    def test_04_11_zeba(self):
        self.assertEqual(self.getHitCounter()('zeba'.encode('utf-8'), self.getSolver(4, 418, (0x7a, 0x61))), 1)
    
    def test_06_10_uscbaa(self):
        self.assertEqual(self.getHitCounter()('uscbaa'.encode('utf-8'), self.getSolver(6, 623, (0x75, 0x61))), 1)
        
    def test_06_10_zscbaa(self):
        self.assertEqual(self.getHitCounter()('zscbaa'.encode('utf-8'), self.getSolver(6, 628, (0x7a, 0x61))), 1)
        
        
    """
        python 3.5:
            9.3-11.0s
    """
    def test_06_10_rrnmeeeaaa(self):
        self.assertEqual(self.getHitCounter()('rrnmeeeaaa'.encode('utf-8'), self.getSolver(10, 1041, (0x72, 0x61))), 1)
        
    def test_16_10_srrrpnmieeeeeaaa(self):
        self.assertEqual(self.getHitCounter()('srrrpnmieeeeeaaa'.encode('utf-8'), self.getSolver(16, 1689, (0x73, 0x61))), 1)
        
        
class Solver_sum_RecursiveOptimized_withInterval_withMedian_V1(Tests.Base.Solver_sum_Words_withCallback):
    def getSolver(self, len, sum, interval, median):
        slv = Solver.sumAndMedian.V1()
        
        # min width: 4+4+2+1 = 11
        slv.setHint('length', len)
        slv.setHint('sum', sum)
        slv.setHint('interval', (max(interval), min(interval)))
        slv.setHint('median', median)
        return slv
        
    """
        python 3.5:
            7.1s, {'md': {'>': 11712, '<': 3438, '=': 18393, }}
            6.2s, {'md': {'>': 4746,  '<': 3438, '=': 18393, }}
            5.7s, {'md': {'>': 4746,  '<': 3181, '=': 18393, }}
            6.7s, after "abstractization", for the Optimized version
    """
    def test_06_10_rrnmeeeaaa(self):
        self.assertEqual(self.getHitCounter()('rrnmeeeaaa'.encode('utf-8'), self.getSolver(10, 1041, (0x72, 0x61), 0x65)), 1)
    
    """
        python 3.5:
            978.9s, {'md': {'>': 114939, '<': 15868, '=': 386149, }}
    """
    def test_16_10_srrrpnmieeeeeaaa(self):
        self.assertEqual(self.getHitCounter()('srrrpnmieeeeeaaa'.encode('utf-8'), self.getSolver(16, 1689, (0x73, 0x61), 0x65)), 1)
        
class Solver_sum_RecursiveOptimized_withInterval_withMedian_Optimized(Tests.Base.Solver_sum_Words_withCallback):
    def getSolver(self, len, sum, interval, median):
        slv = Solver.sumAndMedian.Optimized()
        
        # min width: 4+4+2+1 = 11
        slv.setHint('length', len)
        slv.setHint('sum', sum)
        slv.setHint('interval', (max(interval), min(interval)))
        slv.setHint('median', median)
        return slv
        
    """
        python 3.5:
            1.5s
    """
    def test_06_10_rrnmeeeaaa(self):
        self.assertEqual(self.getHitCounter()('rrnmeeeaaa'.encode('utf-8'), self.getSolver(10, 1041, (0x72, 0x61), 0x65)), 1)
    
    """
        python 3.5:
            260s
    """
    def test_16_10_srrrpnmieeeeeaaa(self):
        self.assertEqual(self.getHitCounter()('srrrpnmieeeeeaaa'.encode('utf-8'), self.getSolver(16, 1689, (0x73, 0x61), 0x65)), 1)
        
"""
class Solver_sumAndMedian_V1(unittest.TestCase):
    def getSolver(self, len, sum, median):
        slv = Solver.sumAndMedian.V1()
        slv.setHint('length', len)
        slv.setHint('sum', sum)
        slv.setHint('median', median)
        return slv
        
    def getCounter(self):
        return countSolverWithCallback
        
    def test_6_s_623(self):
        self.assertEqual(self.getCounter()(self.getSolver(6, 623, 0x62)), 11)

"""

if __name__ == '__main__':
    unittest.main()
    
