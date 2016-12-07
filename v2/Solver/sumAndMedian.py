# -*- coding: utf-8 -*-
import Solver.Base
import Solver.sum
from Solver.Base import CallbackResult

"""
    seems accurate, fast, 0 false-positives
    non-recursive
"""
class V1(Solver.Base.Base):
    def __init__(self):
        super(V1, self).__init__()
        self.callback = None
        self.hints['median'] = None
        self.middleIndex = None
        
        self.stats['md'] = {}
        self.stats['md']['='] = 0
        self.stats['md']['>'] = 0
        self.stats['md']['<'] = 0
        
    
    def solve(self, callback=None):
        slv = Solver.sum.RecursiveOptimized()
        slv.setHint('length', self.hints['length'])
        slv.setHint('sum', self.hints['sum'])
        slv.setHint('interval', self.hints['interval'])
        
        self.middleIndex = self.hints['length']//2
        
        self.callback = callback
        slv.solve(callback=self._evt_sum_solved)
        self.callback = None
        

    def _evt_sum_solved(self, buf, params):
        md = buf[self.middleIndex]
        if md==self.hints['median']:
            self.stats['md']['=']+=1
            return self.callback(buf, params)
        
        if params['depth']>self.middleIndex:
            if md<self.hints['median']:
                self.stats['md']['<']+=1
                #return CallbackResult(params['depth'] - self.middleIndex) # this should be the most exact return
                return CallbackResult(params['depth'] - self.middleIndex+1, self.hints['median'] - md-1) # "optimized"
                #return CallbackResult(params['depth'] - self.middleIndex+1) # "optimized"
            
            elif md>self.hints['median']:
                self.stats['md']['>']+=1
                #return CallbackResult(params['depth'] - self.middleIndex)
                #return CallbackResult(params['depth'] - self.middleIndex, self.hints['median'] - md+1) # "optimized"
                return CallbackResult(params['depth'] - self.middleIndex, md - self.hints['median']-1) # "optimized"
