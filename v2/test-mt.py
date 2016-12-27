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
import Solver.mtBase
#import Solver.sumAndMD5

import multiprocessing

"""
    py ./test-mt.py -v Solver_sum_RecursiveOptimized_withInterval_withSplitPoint_withBinaryDiff_withXorSum_V1.test_26_10

"""
def thread(idx, slv):
    """thread worker function"""
    countSolverHitsWithCallback('vtttssroooniiihfeeddaN    '.encode('utf-8'), slv)
    
DBG = False
def countSolverHitsWithCallback(match, slv):
    def slv_callback(buf, params):
        if DBG:
            print("    %s" % slv.print_tbuf(buf))
        if match==buf:
            print("MATCH FOUND")
            print("    %s" % slv.print_buf_as_str(buf))
            global solutions
            solutions+=1
            
            # fast-return. as a final optimization
            #return (CallbackResult(len(buf)), None, None)
        
   
    if DBG:
        print("")
        print("-"*80)
        print("%s, %d, %d " % (type(slv), slv.hints['length'], slv.hints['sum']))
    
    global solutions
    solutions = 0
    slv.initialize()
    slv.solve(callback=slv_callback)
    slv.destroy()
    
    if DBG:
        print("    solutions: %d" % (solutions))
        
    return solutions

    
class Solver_mtBase_SolverTracer(Tests.Base.Solver_sum_Words_withCallback):
    def getSolver(self, len, sum, interval, index, value, xorsum, binarydiff):
        slv = Solver.mtBase.SolverTracer()
        
        # min width: 4+4+2+2+1+L/8 = 13+L/8
        slv.setHint('length', len)
        slv.setHint('sum', sum)
        slv.setHint('interval', (max(interval), min(interval)))
        slv.setHint('index', index)
        slv.setHint('value', value)
        slv.setHint('xorsum', xorsum)
        slv.setHint('binarydiff', binarydiff)
        
        return slv
        
    def test_26_11_mt(self):
        L = 26
        slv = self.getSolver(L, 2479, (0x76,0x20), 0x15,0x4e, 0x39, (0,1,0,0,1,0,1,1,0,0,1,1,0,0,1,1,1,0,1,0,1,1,1,0,0,0,))
        countSolverHitsWithCallback('vtttssroooniiihfeeddaN    '.encode('utf-8'), slv)
       

if __name__ == '__main__':
    unittest.main()
    
