import sys, time
import argparse
import unittest

import Tests.Base

import Solver.sum
import Solver.sumAndMedian
import Solver.sumAndSplitPoint
import Solver.sumAndSplitPointAndXorSum
import Solver.sumAndSplitPointAndBinaryDiff
import Solver.sumAndSplitPointAndBinaryDiffAndXorSum
#import Solver.sumAndMD5


"""
    py ./test.py -v Solver_sum_RecursiveOptimized_withInterval.test_02_10_ba
    py ./test.py -v Solver_sum_RecursiveOptimized_withInterval.test_04_11_zeba
    py ./test.py -v Solver_sum_RecursiveOptimized_withInterval.test_08_10_zeba
    
    py ./test.py -v Solver_sum_RecursiveOptimized_withInterval_withMedian_V1.test_06_10_rrnmeeeaaa
    
    py ./test.py -v Solver_sum_RecursiveOptimized_withInterval_withMedian_Optimized.test_06_10_rrnmeeeaaa
    
    py ./test.py -v Solver_sum_RecursiveOptimized_withInterval_withSplitPoint_Optimized.test_10_10_rrnmeeeaaa
    py ./test.py -v Solver_sum_RecursiveOptimized_withInterval_withSplitPoint_Optimized.test_12_12_urponneeebaa
    py ./test.py -v Solver_sum_RecursiveOptimized_withInterval_withSplitPoint_Optimized.test_16_10_srrrpnmieeeeeaaa
    py ./test.py -v Solver_sum_RecursiveOptimized_withInterval_withSplitPoint_Optimized.test_16_10_srrrpnmieeeeeaaa_v2
    py ./test.py -v Solver_sum_RecursiveOptimized_withInterval_withSplitPoint_Optimized.test_26_10_srrrrpnmmiieeeeeaaaa
    py ./test.py -v Solver_sum_RecursiveOptimized_withInterval_withSplitPoint_Optimized.test_49_10_vutssssrrrrrpnnnmmiiiiieeeeeeebaaaaaa
    
    
    py ./test.py -v Solver_sum_RecursiveOptimized_withInterval_withSplitPoint_withXorSum_V1.test_16_10_srrrpnmieeeeeaaa
    
    # most optimal
    py ./test.py -v Solver_sum_RecursiveOptimized_withInterval_withSplitPoint_withBinaryDiff_withXorSum_V1.test_16_13
    

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
    def test_08_10_12345678(self):
        self.assertEqual(self.getHitCounter()('12345678'.encode('utf-8'), self.getSolver(6, 628, (0x7a, 0x61))), 1)
            
    def test_08_11_az190AZ_(self):
        self.assertEqual(self.getHitCounter()('az190AZ_'.encode('utf-8'), self.getSolver(6, 628, (0x7a, 0x61))), 1)
    """
        
    """
        python 3.5:
            9.3-11.0s
    """
    def test_10_10_rrnmeeeaaa(self):
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
    def test_10_10_rrnmeeeaaa(self):
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
    def test_10_10_rrnmeeeaaa(self):
        self.assertEqual(self.getHitCounter()('rrnmeeeaaa'.encode('utf-8'), self.getSolver(10, 1041, (0x72, 0x61), 0x65)), 1)
    
    """
        python 3.5:
            260s
    """
    def test_16_10_srrrpnmieeeeeaaa(self):
        self.assertEqual(self.getHitCounter()('srrrpnmieeeeeaaa'.encode('utf-8'), self.getSolver(16, 1689, (0x73, 0x61), 0x65)), 1)
        
        
        
class Solver_sum_RecursiveOptimized_withInterval_withSplitPoint_Optimized(Tests.Base.Solver_sum_Words_withCallback):
    def getSolver(self, len, sum, interval, index, value):
        slv = Solver.sumAndSplitPoint.Optimized()
        
        # min width: 4+4+2+1+1 = 12
        slv.setHint('length', len)
        slv.setHint('sum', sum)
        slv.setHint('interval', (max(interval), min(interval)))
        slv.setHint('index', index)
        slv.setHint('value', value)
        
        return slv
        
    """
        python 3.5:
            1.14
    """
    def test_10_10_rrnmeeeaaa(self):
        self.assertEqual(self.getHitCounter()('rrnmeeeaaa'.encode('utf-8'), self.getSolver(10, 1041, (0x72, 0x61), 0x03, 0x6d)), 1)
    
    """
        python 3.5:
            0.4
    """
    def test_12_10_lkjihgfedcba(self):
        self.assertEqual(self.getHitCounter()('lkjihgfedcba'.encode('utf-8'), self.getSolver(12, 1230, (0x6c, 0x61), 0x06, 0x66)), 1)
    
    """
        python 3.5:
            0.0
    """    
    def test_12_11_ggggggdddaaa(self):
        self.assertEqual(self.getHitCounter()('ggggggdddaaa'.encode('utf-8'), self.getSolver(12, 1209, (0x67, 0x61), 0x05, 0x67)), 1)
        
        
    """
        python 3.5:
            22s
            11.7s
            10.24
    """
    def test_12_12_urponneeebaa(self):
        self.assertEqual(self.getHitCounter()('urponneeebaa'.encode('utf-8'), self.getSolver(12, 1269, (0x75, 0x61), 0x05, 0x6e)), 1)
    
    """
        python 3.5:
            32s
            13.7s
    """
    def test_12_12_urponneeebaa_v2(self):
        self.assertEqual(self.getHitCounter()('urponneeebaa'.encode('utf-8'), self.getSolver(12, 1269, (0x75, 0x61), 0x03, 0x6f)), 1)
        
    """
        python 3.5:
            36s
            15s
    """
    def test_12_12_urponneeebaa_v3(self):
        self.assertEqual(self.getHitCounter()('urponneeebaa'.encode('utf-8'), self.getSolver(12, 1269, (0x75, 0x61), 0x08, 0x65)), 1)
    
    """
        python 3.5:
            118s - de unde e asta scoasa??
            363s
            173s
            151s
             21s - not safe, recOptimiz_V2
    """
    def test_16_10(self):
        self.assertEqual(self.getHitCounter()('srrrpnmieeeeeaaa'.encode('utf-8'), self.getSolver(16, 1689, (0x73, 0x61), 0x07, 0x69)), 1)
     
    # doesn't work, dont know why
    #def test_16_10_srrrpnmieeeeeaaa_v2(self):
    #    self.assertEqual(self.getHitCounter()('srrrpnmieeeeeaaa'.encode('utf-8'), self.getSolver(16, 1689, (0x73, 0x61), 0x08, 0x65)), 1)
    
    """
        python 3.5:
           XXXs - not safe, recOptimiz_V2
    """
    def test_26_10(self):
        self.assertEqual(self.getHitCounter()('srrrrpnmmiieeeeeaaaa.     '.encode('utf-8'), self.getSolver(26, 2320, (0x73, 0x20), 0x13,0x61)), 1)
    
    # too slow
    #def test_49_10(self):
    #    self.assertEqual(self.getHitCounter()('vutssssrrrrrpnnnmmiiiiieeeeeeebaaaaaa?.          '.encode('utf-8'), self.getSolver(49, 4382, (0x76, 0x20), 0x24, 0x61)), 1)
    
    
# NOT USED
class Solver_sum_RecursiveOptimized_withInterval_withSplitPoint_withXorSum_V1(Tests.Base.Solver_sum_Words_withCallback):
    def getSolver(self, len, sum, interval, index, value, xorsum):
        slv = Solver.sumAndSplitPointAndXorSum.V1()
        
        # min width: 4+4+2+1+1 = 12
        slv.setHint('length', len)
        slv.setHint('sum', sum)
        slv.setHint('interval', (max(interval), min(interval)))
        slv.setHint('index', index)
        slv.setHint('value', value)
        slv.setHint('xorsum', xorsum)
        
        return slv
        
    def test_04_10(self):
        self.assertEqual(self.getHitCounter()('cbaa'.encode('utf-8'), self.getSolver(4, 391, (0x63, 0x61), 0x02,0x61, 0x01)), 1)
    def test_06_10(self):
        self.assertEqual(self.getHitCounter()('dcbbaa'.encode('utf-8'), self.getSolver(6, 589, (0x64, 0x61), 0x03,0x62, 0x07)), 1)
    def test_10_10(self):
        self.assertEqual(self.getHitCounter()('rneeedcbaa'.encode('utf-8'), self.getSolver(10, 1018, (0x72, 0x61), 0x05,0x64, 0x1c)), 1)
    def test_12_10(self):
        self.assertEqual(self.getHitCounter()('srrrpnmieeee'.encode('utf-8'), self.getSolver(12, 1297, (0x73, 0x65), 0x06,0x6d, 0x1b)), 1)
    def test_14_10(self):
        self.assertEqual(self.getHitCounter()('srrrpnmieeeeaa'.encode('utf-8'), self.getSolver(14, 1491, (0x73, 0x61), 0x07,0x69, 0x1b)), 1)
        
    def test_16_10(self):
        self.assertEqual(self.getHitCounter()('sssrrrpnmieeeeaa'.encode('utf-8'), self.getSolver(16, 1721, (0x73, 0x61), 0x08,0x6d, 0x1b)), 1)
        
    """
        python 3.5:
             XXs
    """
    def test_16_10(self):
        self.assertEqual(self.getHitCounter()('srrrpnmieeeeeaaa'.encode('utf-8'), self.getSolver(16, 1689, (0x73, 0x61), 0x07,0x69, 0x1f)), 1)
     
    def test_26_10(self):
        self.assertEqual(self.getHitCounter()('srrrrpnmmiieeeeeaaaa.     '.encode('utf-8'), self.getSolver(26, 2320, (0x73, 0x20), 0x13,0x61, 0x06)), 1)
    
    def test_49_10(self):
        self.assertEqual(self.getHitCounter()('vutssssrrrrrpnnnmmiiiiieeeeeeebaaaaaa?.          '.encode('utf-8'), self.getSolver(49, 4382, (0x76, 0x20), 0x24,0x61, 0x64)), 1)
       
        
  
class Solver_sum_RecursiveOptimized_withInterval_withSplitPoint_withBinaryDiff_V1(Tests.Base.Solver_sum_Words_withCallback):
    def getSolver(self, len, sum, interval, index, value, binarydiff):
        slv = Solver.sumAndSplitPointAndBinaryDiff.V1()
        
        # min width: 4+4+2+1+1 = 12
        slv.setHint('length', len)
        slv.setHint('sum', sum)
        slv.setHint('interval', (max(interval), min(interval)))
        slv.setHint('index', index)
        slv.setHint('value', value)
        slv.setHint('binarydiff', binarydiff)
        
        return slv
        
    def test_04_10(self):
        self.assertEqual(self.getHitCounter()('cbaa'.encode('utf-8'), self.getSolver(4, 391, (0x63, 0x61), 0x02,0x61, (0,1,1,0,))), 1)
        
    def test_06_10(self):
        self.assertEqual(self.getHitCounter()('xdcbaa'.encode('utf-8'), self.getSolver(6, 611, (0x78, 0x61), 0x03,0x62, (0,1,1,1,1,0,))), 1)

    """
        python 3.5:
             0.02s
    """
    def test_16_10(self):
        self.assertEqual(self.getHitCounter()('srrrpnmieeeeeaaa'.encode('utf-8'), self.getSolver(16, 1689, (0x73, 0x61), 0x07,0x69, (0,1,0,0,1,1,1,1,1,0,0,0,0,1,0,0,))), 1)
        
    def test_26_10(self):
        self.assertEqual(self.getHitCounter()('srrrrpnmmiieeeeeaaaa.     '.encode('utf-8'), self.getSolver(26, 2320, (0x73, 0x20), 0x13,0x61, (0,1,0,0,0,1,1,1,0,1,0,1,0,0,0,0,1,0,0,0,1,1,0,0,0,0,))), 1)
    
    def test_30_10(self):
        self.assertEqual(self.getHitCounter()('999888777666555444333222111000'.encode('utf-8'), self.getSolver(30, 1575, (0x39, 0x30), 0x0e,0x35,  (0,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,))), 1)
    
    def test_49_10(self):
        self.assertEqual(self.getHitCounter()('vutssssrrrrrpnnnmmiiiiieeeeeeebaaaaaa?.          '.encode('utf-8'), self.getSolver(49, 4382, (0x76, 0x20), 0x24,0x61, (0,1,1,1,0,0,0,1,0,0,0,0,1,1,0,0,1,0,1,0,0,0,0,1,0,0,0,0,0,0,1,1,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,))), 1)
       

class Solver_sum_RecursiveOptimized_withInterval_withSplitPoint_withBinaryDiff_V2(Tests.Base.Solver_sum_Words_withCallback):
    def getSolver(self, len, sum, interval, index, value, binarydiff):
        slv = Solver.sumAndSplitPointAndBinaryDiff.V2()
        
        # min width: 4+4+2+1+1 = 12
        slv.setHint('length', len)
        slv.setHint('sum', sum)
        slv.setHint('interval', (max(interval), min(interval)))
        slv.setHint('index', index)
        slv.setHint('value', value)
        slv.setHint('binarydiff', binarydiff)
        
        return slv
        
    def test_04_10(self):
        self.assertEqual(self.getHitCounter()('cbaa'.encode('utf-8'), self.getSolver(4, 391, (0x63, 0x61), 0x02,0x61, (0,1,1,0,))), 1)
        
    def test_06_10(self):
        self.assertEqual(self.getHitCounter()('xdcbaa'.encode('utf-8'), self.getSolver(6, 611, (0x78, 0x61), 0x03,0x62, (0,1,1,1,1,0,))), 1)
    
    """
        python 3.5:
             0.03s
    """
    def test_16_10(self):
        self.assertEqual(self.getHitCounter()('srrrpnmieeeeeaaa'.encode('utf-8'), self.getSolver(16, 1689, (0x73, 0x61), 0x07,0x69, (0,1,0,0,1,1,1,1,1,0,0,0,0,1,0,0,))), 1)

    """
        python 3.5:
             0.01s
    """        
    def test_16_11(self):
        self.assertEqual(self.getHitCounter()('zaaaaaaaaaaaaaaa'.encode('utf-8'), self.getSolver(16, 1577, (0x7a,0x61), 0x08,0x61, (0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,))), 1)
        
    """
        python 3.5:
             0.041s
    """
    def test_16_12(self):
        """ 
            --splitPoint=0x08,0x64 (@8, d)
                                     'zjihgfeeddccbaaa'
            --binarydiff              0111111010101100
              offsets                 0123456789012345
            -> binaryDiffRSums        aa98765443322100
                                      .......|^|......

        """
        self.assertEqual(self.getHitCounter()('zjihgfeeddccbaaa'.encode('utf-8'), self.getSolver(16, 1631, (0x7a,0x61), 0x08,0x64, (0,1,1,1,1,1,1,0,1,0,1,0,1,1,0,0,))), 1)
    
    """
        python 3.5:
            1.630s
            1.84s
    """
    def test_16_13(self):
        self.assertEqual(self.getHitCounter()('zyxvutsqomkigeca'.encode('utf-8'), self.getSolver(16, 1774, (0x7a,0x61), 0x08,0x6f, (0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,))), 1)
    
    """
        python 3.5:
            20.0s
            9.7s
            5.5s
    """
    def test_16_15(self):
        """ 
            --splitPoint==0x0d,0x61 (@13, a)
                                     'zsrrrpnmieeaaa  '
            --binarydiff              0110011111010010
              offsets                 0123456789012345
            -> binaryDiffRSums        9987776543221110
            -> binaryDiffRSumsV2      9877765432211100
                                      .............^..

        """
        # the splitpoint analizer fails for this case. It should return something different
        self.assertEqual(self.getHitCounter()('zsrrrpnmieeaaa  '.encode('utf-8'), self.getSolver(16, 1572, (0x7a,0x20), 0x0d,0x61, (0,1,1,0,0,1,1,1,1,1,0,1,0,0,1,0,))), 1)
        
        # different split points
        #self.assertEqual(self.getHitCounter()('zsrrrpnmieeaaa  '.encode('utf-8'), self.getSolver(16, 1572, (0x7a,0x20), 13,ord('a'), (0,1,1,0,0,1,1,1,1,1,0,1,0,0,1,0,))), 1)
        #self.assertEqual(self.getHitCounter()('zsrrrpnmieeaaa  '.encode('utf-8'), self.getSolver(16, 1572, (0x7a,0x20), 11,ord('a'), (0,1,1,0,0,1,1,1,1,1,0,1,0,0,1,0,))), 1)
     
    """
        python 3.5:
            7.1s
            6.8s
    """
    def test_26_10(self):
        """ 
            --splitPoint=0x13,0x61 (@19, a)
                                     'srrrrpnmmiieeeeeaaaa.     '
            --binarydiff              01000111010100001000110000
              offsets                 01234567890123456789012345
            -> binaryDiffRSums        99888876554433333222210000
            -> binaryDiffRSumsV2      98888765544333332222100000
                                      ...................^......
        """
        self.assertEqual(self.getHitCounter()('srrrrpnmmiieeeeeaaaa.     '.encode('utf-8'), self.getSolver(26, 2320, (0x73, 0x20), 0x13,0x61, (0,1,0,0,0,1,1,1,0,1,0,1,0,0,0,0,1,0,0,0,1,1,0,0,0,0,))), 1)
    
    
    """
        python 3.5:
            176s (with diff split point)
    """
    def test_26_11(self):
        """ 
            --splitPoint=0x15,0x4e (@21, N)
                                     'vtttssroooniiihfeeddaN    '
            --binarydiff              01001011001100111010111000
              offsets                 01234567890123456789012345
            -> binaryDiffRSums        ddcccbba999877765443321000
            -> binaryDiffRSumsV2      dcccbba9998777654433210000
                                      .....................^....
        """
        #self.assertEqual(self.getHitCounter()('vtttssroooniiihfeeddaN    '.encode('utf-8'), self.getSolver(26, 2479, (0x76,0x20), 0x15,0x4e, (0,1,0,0,1,0,1,1,0,0,1,1,0,0,1,1,1,0,1,0,1,1,1,0,0,0,))), 1)
        self.assertEqual(self.getHitCounter()('vtttssroooniiihfeeddaN    '.encode('utf-8'), self.getSolver(26, 2479, (0x76,0x20), 20,ord('a'), (0,1,0,0,1,0,1,1,0,0,1,1,0,0,1,1,1,0,1,0,1,1,1,0,0,0,))), 1)
    
    
    #def test_30_10(self):
    #    self.assertEqual(self.getHitCounter()('999888777666555444333222111000'.encode('utf-8'), self.getSolver(30, 1575, (0x39, 0x30), 0x0e,0x35,  (0,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,))), 1)
    
    #def test_49_10(self):
    #    self.assertEqual(self.getHitCounter()('vutssssrrrrrpnnnmmiiiiieeeeeeebaaaaaa?.          '.encode('utf-8'), self.getSolver(49, 4382, (0x76, 0x20), 0x24,0x61, (0,1,1,1,0,0,0,1,0,0,0,0,1,1,0,0,1,0,1,0,0,0,0,1,0,0,0,0,0,0,1,1,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,))), 1)
       

class Solver_sum_RecursiveOptimized_withInterval_withSplitPoint_withBinaryDiff_withXorSum_V1(Tests.Base.Solver_sum_Words_withCallback):
    def getSolver(self, len, sum, interval, index, value, xorsum, binarydiff):
        slv = Solver.sumAndSplitPointAndBinaryDiffAndXorSum.V1()
        
        # min width: 4+4+2+2+1+L/8 = 13+L/8
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
    
    """
        python 3.5: 
            0.760s
    """
    def test_16_13(self):
        self.assertEqual(self.getHitCounter()('zyxvutsqomkigeca'.encode('utf-8'), self.getSolver(16, 1774, (0x7a,0x61), 0x08,0x6f, 0x0e, (0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,))), 1)
    
    """
        python 3.5: 
            6.490s
    """
    def test_16_15(self):
        # the splitpoint analizer fails for this case. It should return something different
        self.assertEqual(self.getHitCounter()('zsrrrpnmieeaaa  '.encode('utf-8'), self.getSolver(16, 1572, (0x7a,0x20), 0x0d,0x61, 0x00, (0,1,1,0,0,1,1,1,1,1,0,1,0,0,1,0,))), 1)
        
    """
        python 3.5: 
            8.840s
    """
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
    
