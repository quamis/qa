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
                ret+=("    %s %02d: @0x%02x (0x%02x-0x%02x)... sum:%d, xor:0x%02x\n" % (
                    (">" if offset==coffset else "~"), 
                    offset,
                    stk[0],
                    stk[3],
                    stk[4],
                    stk[1],
                    stk[2],
                ))
        return ret
        
    def print_solFromStack(self, stack, coffset=None):
        ret = ""
        for (offset, stk) in enumerate(stack):
            if stk:
                ret+=("%c" % (stk[0]))
        return ret
        
    def _spawn(self, maxoffset):
        # clone the stack
        nstack = []
        for stk in self._stack:
            if stk:
                nstack.append(stk[:])
        
        split = False
        for (offset, stk) in enumerate(nstack):
            if offset<maxoffset:
                if (stk[0]-stk[4])>2:   # c - cmin
                    #print("current stack")
                    #print(self.print_stack(self._stack, offset))
                    
                    mid = (stk[0] - stk[4])//2
                    
                    self._stack[offset][4] = stk[4] + mid # cmin
                    
                    nstack[offset][3] = stk[4] + mid    # cmax
                    nstack[offset][0] = stk[4] + mid    # c
                    
                    for o in range(offset, self.hints['length']-1):
                        nstack[o] = None
                    
                    # TODO: in nstack, handle leftover sum's & xor's in the right of the offset

                    #print("current stack")
                    #print(self.print_stack(self._stack, offset))
                    #print("new stack")
                    #print(self.print_stack(nstack, offset))
                    split = True
                    break
        
        if split:
            # spawn new thread
            print(self.print_solFromStack(self._stack))
            self._stack = nstack
            
        
        return split
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
