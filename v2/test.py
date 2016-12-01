import sys, time
import argparse
import unittest

import Solver.sum
import Solver.sumAndMD5

DBG=False

def countSolver(slv, len, sum):
    slv.setHint('length', len)
    slv.setHint('sum', sum)
   
    if DBG:
        print("")
        print("-"*80)
        print("%s, %d, %d " % (type(slv), len, sum))
    
    solutions = 0
    for s in slv.solve():
        if DBG:
            print("    %s" % slv.print_tbuf(s))
        solutions+=1
    
    if DBG:
        print("    solutions: %d" % (solutions))
    return solutions
    
def countCallbackSolver(slv, len, sum):
    slv.setHint('length', len)
    slv.setHint('sum', sum)
    
    def slv_callback(s):
        if DBG:
            print("    %s" % slv.print_tbuf(s))
        global solutions
        solutions+=1
   
    if DBG:
        print("")
        print("-"*80)
        print("%s, %d, %d " % (type(slv), len, sum))
    
    global solutions
    solutions = 0
    slv.solve(callback=slv_callback)
    
    if DBG:
        print("    solutions: %d" % (solutions))
    return solutions
    

"""
    >>>py ./test.py -v 2>&1 >test_04_x.log
    
    py ./test.py -v Solver_sum_V3_1_vs_V1.test_02_x >test_vs.log
    py ./test.py -v Solver_sum_V3_1_vs_V1.test_03_x >test_vs.log
    py ./test.py -v Solver_sum_V3_1_vs_V1.test_04_x >test_vs.log
    
    
    py ./test.py -v Solver_sum_V3_1.test_3_6
"""

class Solver_sum_VX(unittest.TestCase):
    def getSolver(self):
        pass
        
        
    def getCounter(self):
        return countSolver
        
    def test_2_1(self):
        self.assertEqual(self.getCounter()(self.getSolver(), 2, 1), 1)
        
    def test_2_2(self):
        self.assertEqual(self.getCounter()(self.getSolver(), 2, 2), 2)
        
    def test_2_3(self):
        self.assertEqual(self.getCounter()(self.getSolver(), 2, 3), 2)
        
    def test_2_4(self):
        self.assertEqual(self.getCounter()(self.getSolver(), 2, 4), 3)
        
    def test_2_5(self):
        self.assertEqual(self.getCounter()(self.getSolver(), 2, 5), 3)
        
    def test_2_6(self):
        self.assertEqual(self.getCounter()(self.getSolver(), 2, 6), 4)
        
    def test_2_7(self):
        self.assertEqual(self.getCounter()(self.getSolver(), 2, 7), 4)
        
    def test_2_8(self):
        self.assertEqual(self.getCounter()(self.getSolver(), 2, 8), 5)
        
    def test_2_9(self):
        self.assertEqual(self.getCounter()(self.getSolver(), 2, 9), 5)
        
        
    def test_2_z_0x01(self):
        self.assertEqual(self.getCounter()(self.getSolver(), 2, 0x01), 1)
        
    def test_2_z_0x02(self):
        self.assertEqual(self.getCounter()(self.getSolver(), 2, 0x02), 2)
        
    def test_2_z_0x04(self):
        self.assertEqual(self.getCounter()(self.getSolver(), 2, 0x04), 3)
        
    def test_2_z_0x0f(self):
        self.assertEqual(self.getCounter()(self.getSolver(), 2, 0x0f), 8)
        
    def test_2_z_0x1f(self):
        self.assertEqual(self.getCounter()(self.getSolver(), 2, 0x1f), 16)
        
    def test_2_z_0xffd2(self):
        self.assertEqual(self.getCounter()(self.getSolver(), 2, 0xff//2), 64)
        
    def test_2_z_0xffd2a1(self):
        self.assertEqual(self.getCounter()(self.getSolver(), 2, 0xff//2+1), 65)
        
    def test_2_z_0xffd2a2(self):
        self.assertEqual(self.getCounter()(self.getSolver(), 2, 0xff//2+2), 65)
        
    def test_2_z_0xffm2d2(self):
        self.assertEqual(self.getCounter()(self.getSolver(), 2, 0xff*2//2), 128)
        
    def test_2_z_0xffm2s2(self):
        self.assertEqual(self.getCounter()(self.getSolver(), 2, 0xff*2-2), 2)
        
    def test_2_z_0xffm2s1(self):
        self.assertEqual(self.getCounter()(self.getSolver(), 2, 0xff*2-1), 1)
        
    def test_2_z_0xffm2(self):
        self.assertEqual(self.getCounter()(self.getSolver(), 2, 0xff*2), 1)
        

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def test_3_1(self):
        self.assertEqual(self.getCounter()(self.getSolver(), 3, 1), 1)
        
    def test_3_2(self):
        self.assertEqual(self.getCounter()(self.getSolver(), 3, 2), 2)
        
    def test_3_3(self):
        self.assertEqual(self.getCounter()(self.getSolver(), 3, 3), 3)
        
    def test_3_4(self):
        self.assertEqual(self.getCounter()(self.getSolver(), 3, 4), 4)
        
    def test_3_5(self):
        self.assertEqual(self.getCounter()(self.getSolver(), 3, 5), 5)
        
    def test_3_6(self):
        self.assertEqual(self.getCounter()(self.getSolver(), 3, 6), 7)
        
    def test_3_7(self):
        self.assertEqual(self.getCounter()(self.getSolver(), 3, 7), 8)
        
    def test_3_8(self):
        self.assertEqual(self.getCounter()(self.getSolver(), 3, 8), 10)
        
    def test_3_9(self):
        self.assertEqual(self.getCounter()(self.getSolver(), 3, 9), 12)
        
        
    def test_3_0x08f(self):
        self.assertEqual(self.getCounter()(self.getSolver(), 3, 0x8f), 1776)
        
    def test_3_0x0f8(self):
        self.assertEqual(self.getCounter()(self.getSolver(), 3, 0xf8), 5250)
        
    def test_3_0x0ff(self):
        self.assertEqual(self.getCounter()(self.getSolver(), 3, 0xff), 5547)
        

   #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def test_4_1(self):
        self.assertEqual(self.getCounter()(self.getSolver(), 4, 1), 1)
        
    def test_4_2(self):
        self.assertEqual(self.getCounter()(self.getSolver(), 4, 2), 2)
        
    def test_4_3(self):
        self.assertEqual(self.getCounter()(self.getSolver(), 4, 3), 3)
        
    def test_4_4(self):
        self.assertEqual(self.getCounter()(self.getSolver(), 4, 4), 5)
        
    def test_4_5(self):
        self.assertEqual(self.getCounter()(self.getSolver(), 4, 5), 6)
        
    def test_4_6(self):
        self.assertEqual(self.getCounter()(self.getSolver(), 4, 6), 9)
        
    def test_4_7(self):
        self.assertEqual(self.getCounter()(self.getSolver(), 4, 7), 11)
        
    def test_4_8(self):
        self.assertEqual(self.getCounter()(self.getSolver(), 4, 8), 15)
        
    def test_4_9(self):
        self.assertEqual(self.getCounter()(self.getSolver(), 4, 9), 18)
        
        
        
    def test_4_z_0x01(self):
        self.assertEqual(self.getCounter()(self.getSolver(), 4, 0x01), 1)
        
    def test_4_z_0x02(self):
        self.assertEqual(self.getCounter()(self.getSolver(), 4, 0x02), 2)
        
    def test_4_z_0x04(self):
        self.assertEqual(self.getCounter()(self.getSolver(), 4, 0x04), 5)
        
    def test_4_z_0x0f(self):
        self.assertEqual(self.getCounter()(self.getSolver(), 4, 0x0f), 54)
        
    def test_4_z_0x1f(self):
        self.assertEqual(self.getCounter()(self.getSolver(), 4, 0x1f), 321)
        
    def test_4_z_0xffd2(self):
        self.assertEqual(self.getCounter()(self.getSolver(), 4, 0xff//2), 15961)
        
    def test_4_z_0xffd2a1(self):
        self.assertEqual(self.getCounter()(self.getSolver(), 4, 0xff//2+1), 16335)
        
    def test_4_z_0xffd2a2(self):
        self.assertEqual(self.getCounter()(self.getSolver(), 4, 0xff//2+2), 16698)
        
    def test_4_z_0xffm2d2(self):
        self.assertEqual(self.getCounter()(self.getSolver(), 4, 0xff*4//2), 474290)
        
    def test_4_z_0xffm2s2(self):
        self.assertEqual(self.getCounter()(self.getSolver(), 4, 0xff*4-2), 2)
        
    def test_4_z_0xffm2s1(self):
        self.assertEqual(self.getCounter()(self.getSolver(), 4, 0xff*4-1), 1)
        
    def test_4_z_0xffm2(self):
        self.assertEqual(self.getCounter()(self.getSolver(), 4, 0xff*4), 1)
        

class Solver_sum_VX_withCallback(Solver_sum_VX):
    def getSolver(self):
        pass
        
    def getCounter(self):
        return countCallbackSolver
    
    
    
class Solver_sum_V1(Solver_sum_VX):
    def getSolver(self):
        return Solver.sum.V1()
        
class Solver_sum_V1_1(Solver_sum_VX):
    def getSolver(self):
        return Solver.sum.V1_1()

class Solver_sum_V1_3(Solver_sum_VX_withCallback):
    def getSolver(self):
        return Solver.sum.V1_3()
        
class Solver_sum_V3(Solver_sum_VX):
    def getSolver(self):
        return Solver.sum.V3()
        
class Solver_sum_V3_1(Solver_sum_VX):
    def getSolver(self):
        return Solver.sum.V3_1()

        


if __name__ == '__main__':
    unittest.main()
    
    
    