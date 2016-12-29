# -*- coding: utf-8 -*-
import sys, time

import Solver.NRSumAndSplitPointAndBinaryDiffAndXorSum

class SolverTracer(Solver.NRSumAndSplitPointAndBinaryDiffAndXorSum.V1):  
    def __init__(self):
        super(SolverTracer, self).__init__()
        
        # settings
        self.settings['warmup_time'] = 2
        self.settings['reportProgress_time'] = 1
        
        self.settings['maxProcesses'] = 4
        
        # settings
        self.stats['processes'] = []
        
        self.stats['solve::start'] = 0
        
        self.stats['_computeLimits::returns'] = []
        self.stats['_computeLimits::calls'] = 0
        self.stats['_computeLimits::reportingInterval'] = None
        
        
    def solve(self, callback=None):
        self.stats['solve::start'] = time.time()
        
        for i in range(self.hints['length']):
            self.stats['_computeLimits::returns'].append(self.stats['solve::start'])
        
        return super(SolverTracer, self).solve(callback)

    def print_stack(self, stack, coffset=None):
        ret = ""
        for (offset, stk) in enumerate(stack):
            if stk:
                ret+=("\n    %s %02d: @0x%02x (0x%02x-0x%02x)... sum:%d, xor:0x%02x" % (
                    (">" if offset==coffset else "~"), 
                    offset,
                    stk[0],
                    stk[3],
                    stk[4],
                    stk[1],
                    stk[2],
                ))
        return ret
        
    def _spawn(self, maxoffset):
        print(self._precalc__computeLimits)
        print(self._stack)
        nstack = self._stack[:]
        for (offset, stk) in enumerate(self._stack):
            if offset<maxoffset:
                if (stk[0]-stk[4])>1:   # c - cmin
                    nstack[offset][0]-=1
                    print(" >> %d" % (offset))
                    print(self.print_stack(nstack, offset))
                    break
        exit()
        return False
        #return self.callbackProgress(tbuf, {})
        
    def _computeLimits(self, offset, cc):
        r = super(SolverTracer, self)._computeLimits(offset, cc)
        self.stats['_computeLimits::returns'][offset] = time.time()
        
        # handle time slices, to check for new thread space availability
        self.stats['_computeLimits::calls']+= 1
        if self.stats['_computeLimits::reportingInterval']:
            if self.stats['_computeLimits::calls']>self.stats['_computeLimits::reportingInterval']:
                if self._spawn(offset):
                    self.stats['_computeLimits::calls'] = 0
        elif self.stats['_computeLimits::calls']%5000==0 and (time.time() - self.stats['solve::start'])>self.settings['warmup_time']:
            self.stats['_computeLimits::reportingInterval'] = (self.stats['_computeLimits::calls']//self.settings['warmup_time'])*self.settings['reportProgress_time']
            #self.stats['_computeLimits::calls'] = 0
        
        return r
