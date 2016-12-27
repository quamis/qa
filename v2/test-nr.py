import sys, time
import argparse
import unittest

import Tests.Base

import Solver.NRSumAndSplitPointAndBinaryDiffAndXorSum


"""
    py test-nr.py -v Solver_NRSumAndSplitPointAndBinaryDiffAndXorSum_V1.test_04_10
"""

class Solver_NRSumAndSplitPointAndBinaryDiffAndXorSum_V1(Tests.Base.Solver_sum_Words_withCallback):
    def getSolver(self, len, sum, interval, index, value, xorsum, binarydiff):
        slv = Solver.NRSumAndSplitPointAndBinaryDiffAndXorSum.V1()
        
        slv.setHint('length', len)
        slv.setHint('sum', sum)
        slv.setHint('interval', (max(interval), min(interval)))
        slv.setHint('index', index)
        slv.setHint('value', value)
        slv.setHint('xorsum', xorsum)
        slv.setHint('binarydiff', binarydiff)
        
        return slv
        
    def test_04_10(self):
        self.assertEqual(self.getHitCounter()('cbaa'.encode('utf-8'), self.getSolver(4, 391, (0x63, 0x61), 0x02,0x61, 0x01, (0,1,1,0,))), 1)
        
    def test_06_10(self):
        self.assertEqual(self.getHitCounter()('xdcbaa'.encode('utf-8'), self.getSolver(6, 611, (0x78, 0x61), 0x03,0x62, 0x1d, (0,1,1,1,1,0,))), 1)
        
    def test_06_11(self):
        self.assertEqual(self.getHitCounter()('xqkgda'.encode('utf-8'), self.getSolver(6, 640, (0x78,0x61), 0x03,0x67, 0x00, (0,1,1,1,1,1,))), 1)
        
    def test_16_10(self):
        self.assertEqual(self.getHitCounter()('srrrpnmieeeeeaaa'.encode('utf-8'), self.getSolver(16, 1689, (0x73,0x61), 0x07,0x69, 0x1f, (0,1,0,0,1,1,1,1,1,0,0,0,0,1,0,0,))), 1)

    def test_16_11(self):
        self.assertEqual(self.getHitCounter()('zaaaaaaaaaaaaaaa'.encode('utf-8'), self.getSolver(16, 1577, (0x7a,0x61), 0x08,0x61, 0x1b, (0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,))), 1)
        
    def test_16_12(self):
        self.assertEqual(self.getHitCounter()('zjihgfeeddccbaaa'.encode('utf-8'), self.getSolver(16, 1631, (0x7a,0x61), 0x08,0x64, 0x13, (0,1,1,1,1,1,1,0,1,0,1,0,1,1,0,0,))), 1)
    
    def test_16_13(self):
        self.assertEqual(self.getHitCounter()('zyxvutsqomkigeca'.encode('utf-8'), self.getSolver(16, 1774, (0x7a,0x61), 0x08,0x6f, 0x0e, (0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,))), 1)
    
    def test_16_15(self):
        # the splitpoint analizer fails for this case. It should return something different
        self.assertEqual(self.getHitCounter()('zsrrrpnmieeaaa  '.encode('utf-8'), self.getSolver(16, 1572, (0x7a,0x20), 0x0d,0x61, 0x00, (0,1,1,0,0,1,1,1,1,1,0,1,0,0,1,0,))), 1)
        
    def test_26_10(self):
        self.assertEqual(self.getHitCounter()('srrrrpnmmiieeeeeaaaa.     '.encode('utf-8'), self.getSolver(26, 2320, (0x73, 0x20), 0x13,0x61, 0x06, (0,1,0,0,0,1,1,1,0,1,0,1,0,0,0,0,1,0,0,0,1,1,0,0,0,0,))), 1)
    
    def test_26_11(self):
        self.assertEqual(self.getHitCounter()('vtttssroooniiihfeeddaN    '.encode('utf-8'), self.getSolver(26, 2479, (0x76,0x20), 0x15,0x4e, 0x39, (0,1,0,0,1,0,1,1,0,0,1,1,0,0,1,1,1,0,1,0,1,1,1,0,0,0,))), 1)
    #    self.assertEqual(self.getHitCounter()('vtttssroooniiihfeeddaN    '.encode('utf-8'), self.getSolver(26, 2479, (0x76,0x20), 20,ord('a'), 0x39, (0,1,0,0,1,0,1,1,0,0,1,1,0,0,1,1,1,0,1,0,1,1,1,0,0,0,))), 1)
    
    def test_62_10(self):
        self.assertEqual(self.getHitCounter()('yywuuuttttttssrrrrpoooooonnnnmlllihhecbaaUTTH44310.-)(        '.encode('utf-8'), self.getSolver(62, 5555, (0x79,0x20), 0x20,0x6c, 0x53, (0,0,1,1,0,0,1,0,0,0,0,0,1,0,1,0,0,0,1,1,0,0,0,0,0,1,0,0,0,1,1,0,0,1,1,0,1,1,1,1,0,1,1,0,1,1,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,))), 1)
  
    def test_62_10_complexity(self):
        # self.assertEqual(self.getHitCounter()('yywuuuttttttssrrrrpoooooonnnnmlllihhecbaaUTTH44310.-)(        '.encode('utf-8'), 
        slv = self.getSolver(62, 5555, (0x79,0x20), 0x20,0x6c, 0x53, (0,0,1,1,0,0,1,0,0,0,0,0,1,0,1,0,0,0,1,1,0,0,0,0,0,1,0,0,0,1,1,0,0,1,1,0,1,1,1,1,0,1,1,0,1,1,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,))
        paralelizationPoints = slv.determineParalelizationPoints()
        #print(paralelizationPoints)
  
          
  

if __name__ == '__main__':
    unittest.main()
    
