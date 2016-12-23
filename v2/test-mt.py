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

class Solver_sum_RecursiveOptimized_withInterval_withSplitPoint_withBinaryDiff_withXorSum_V1(Tests.Base.Solver_sum_Words_withCallback):
    def getSolver(self, len, sum, interval, index, value, xorsum, binarydiff, finalValues):
        slv = Solver.sumAndSplitPointAndBinaryDiffAndXorSum.V1()
        
        # min width: 4+4+2+2+1+L/8 = 13+L/8
        slv.setHint('length', len)
        slv.setHint('sum', sum)
        slv.setHint('interval', (max(interval), min(interval)))
        slv.setHint('index', index)
        slv.setHint('value', value)
        slv.setHint('xorsum', xorsum)
        slv.setHint('binarydiff', binarydiff)
        slv.setHint('finalValues', finalValues)
        
        return slv
        
    def test_26_11(self):
        self.assertEqual(self.getHitCounter()('vtttssroooniiihfeeddaN    '.encode('utf-8'), self.getSolver(26, 2479, (0x76,0x20), 0x15,0x4e, 0x39, (0,1,0,0,1,0,1,1,0,0,1,1,0,0,1,1,1,0,1,0,1,1,1,0,0,0,), ())), 1)
    #    self.assertEqual(self.getHitCounter()('vtttssroooniiihfeeddaN    '.encode('utf-8'), self.getSolver(26, 2479, (0x76,0x20), 20,ord('a'), 0x39, (0,1,0,0,1,0,1,1,0,0,1,1,0,0,1,1,1,0,1,0,1,1,1,0,0,0,))), 1)
    
    def test_26_11_complexity(self):
        paralelizationPoints = self.getSolver(26, 2479, (0x76,0x20), 0x15,0x4e, 0x39, (0,1,0,0,1,0,1,1,0,0,1,1,0,0,1,1,1,0,1,0,1,1,1,0,0,0,), ()).determineParalelizationPoints()
        print(paralelizationPoints)
        
    def test_26_11_mt(self):
        L = 26
        paralelizationPoints = self.getSolver(L, 2479, (0x76,0x20), 0x15,0x4e, 0x39, (0,1,0,0,1,0,1,1,0,0,1,1,0,0,1,1,1,0,1,0,1,1,1,0,0,0,), ()).determineParalelizationPoints()
        #print(paralelizationPoints)
        
        
        jobslices = 2
        finalValuesForJobs = []
        p = paralelizationPoints[0]
        print(p['interval'])
        iSize = (p['interval'][0]-p['interval'][1])//jobslices
        for j in range(0, jobslices-1):
            finalValues = [None]*L
            finalValues[p['offset']] = ( p['interval'][0]-(j*iSize), p['interval'][0]-((j+1)*iSize)+1,)
            finalValuesForJobs.append(finalValues)
            
        finalValues = [None]*L
        finalValues[p['offset']] = ( p['interval'][0]-((jobslices-1)*iSize), p['interval'][1],)
        finalValuesForJobs.append(finalValues)
            
        solvers = []
        for finalValues in finalValuesForJobs:
            solvers.append(self.getSolver(L, 2479, (0x76,0x20), 0x15,0x4e, 0x39, (0,1,0,0,1,0,1,1,0,0,1,1,0,0,1,1,1,0,1,0,1,1,1,0,0,0,), finalValues))
        
        jobs = []
        for (idx, slv) in enumerate(solvers):
            p = multiprocessing.Process(target=thread, args=(idx, slv,))
            jobs.append(p)
            p.start()
            
        for p in jobs:
            p.join()
            print('{:>15}.exitcode = {}'.format(p.name, p.exitcode))
        
        #self.assertEqual(self.getHitCounter()('vtttssroooniiihfeeddaN    '.encode('utf-8'), self.getSolver(L, 2479, (0x76,0x20), 0x15,0x4e, 0x39, (0,1,0,0,1,0,1,1,0,0,1,1,0,0,1,1,1,0,1,0,1,1,1,0,0,0,), finalValues)), 1)

class Solver_sum_RecursiveOptimized_withInterval_withSplitPoint_withBinaryDiff_withXorSum_V1_mt(Tests.Base.Solver_sum_Words_withCallback):
    def getSolver(self, len, sum, interval, index, value, xorsum, binarydiff):
        slv = Solver.sumAndSplitPointAndBinaryDiffAndXorSum.V1_mt()
        
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
    
