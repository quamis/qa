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
    
    
class Solver_sum_VX(unittest.TestCase):
    def getSolver(self):
        pass
        
    def test_02_x(self):
        for s in range(0, 1+0xff*2):
            self.assertNotEqual(countSolver(self.getSolver(), 2, s), 0)
            
    def test_03_x(self):
        for s in range(0, 1+0xff*3):
            self.assertNotEqual(countSolver(self.getSolver(), 3, s), 0)
            
            
class Solver_sum_VX_withCallback(unittest.TestCase):
    def getSolver(self):
        pass
        
    def test_02_x(self):
        for s in range(0, 1+0xff*2):
            self.assertNotEqual(countCallbackSolver(self.getSolver(), 2, s), 0)
            
    def test_03_x(self):
        for s in range(0, 1+0xff*3):
            self.assertNotEqual(countCallbackSolver(self.getSolver(), 3, s), 0)
    
"""
    >>>py ./test.py -v 2>&1 >test_04_x.log
    
    py ./test.py -v Solver_sum_V3_1_vs_V1.test_02_x >test_vs.log
    py ./test.py -v Solver_sum_V3_1_vs_V1.test_03_x >test_vs.log
    py ./test.py -v Solver_sum_V3_1_vs_V1.test_04_x >test_vs.log
"""
class Solver_sum_V1(Solver_sum_VX):
    def getSolver(self):
        return Solver.sum.V1()
        
class Solver_sum_V1_1(Solver_sum_VX):
    def getSolver(self):
        return Solver.sum.V1_1()
        
class Solver_sum_V1_2(Solver_sum_VX):
    def getSolver(self):
        return Solver.sum.V1_2()
        
class Solver_sum_V1_3(Solver_sum_VX_withCallback):
    def getSolver(self):
        return Solver.sum.V1_3()
        
class Solver_sum_V3(Solver_sum_VX):
    def getSolver(self):
        return Solver.sum.V3()
        
class Solver_sum_V3_1_vs_V1(unittest.TestCase):
    def test_02_x(self):
        for s in range(0, 1+0xff*2):
            self.assertEqual(countSolver(Solver.sum.V1(), 2, s), countSolver(Solver.sum.V3_1(), 2, s))
    
    
    def test_03_x(self):
        for s in range(0, 1+0xff*3):
            self.assertEqual(countSolver(Solver.sum.V1(), 3, s), countSolver(Solver.sum.V3_1(), 3, s))
    
    
    """
    def test_04_x(self):
        for s in range(0, 1+0xff*4):
            self.assertEqual(countSolver(Solver.sum.V1(), 4, s), countSolver(Solver.sum.V3(), 4, s))
    """
    
    """
    def test_05_x(self):
        for s in range(0, 1+0xff*5):
            self.assertEqual(countSolver(Solver.sum.V1(), 5, s), countSolver(Solver.sum.V3(), 5, s))
            
    def test_06_x(self):
        for s in range(0, 1+0xff*6):
            self.assertEqual(countSolver(Solver.sum.V1(), 6, s), countSolver(Solver.sum.V3(), 6, s))
            
    def test_09_x(self):
        for s in range(0, 1+0xff*9):
            self.assertEqual(countSolver(Solver.sum.V1(), 9, s), countSolver(Solver.sum.V3(), 9, s))
    """
    
if __name__ == '__main__':
    unittest.main()
    
    
    