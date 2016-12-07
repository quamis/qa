# -*- coding: utf-8 -*-
import sys

import Solver.Base
from Solver.Base import CallbackResult

"""
slow, non-optimal
generates ALL combinations, not only in decreasing-sort-order
recursive
"""
class Recursive(Solver.Base.Base):
    def __init__(self):
        super(Recursive, self).__init__()
        self.stats['_generate_tbuf_fromsum:found'] = 0
        self.stats['_generate_tbuf_fromsum:calls'] = 0
        self.stats['_generate_tbuf_fromsum:misses:overflow'] = 0
    
    def solve(self):
        # temporary data buffer
        tbuf = bytearray([0]*self.hints['length'])
        
        for t in self._generate_tbuf_fromsum(tbuf[:], self.hints['sum'], 0, 0xff):
            #print(t)
            #print("\r%s\r" % self.stats)
            #if sum(t)==self.hints['sum']: # 
            #    yield t
            yield t
        #print("done")
        #print(self.stats)
    
    def _generate_tbuf_fromsum(self, tbuf, sum, offset, cc):
        self.stats['_generate_tbuf_fromsum:calls']+= 1
        if sum==0:
            self.stats['_generate_tbuf_fromsum:found']+= 1
            #self.print_tbuf(tbuf)
            yield tbuf
            
        if offset>=self.hints['length']:
            self.stats['_generate_tbuf_fromsum:misses:overflow']+= 1
            return
        
        for c in range(min(0xff, sum, cc), 0x00, -1):
            tbuf[offset] = c
            # propagate found solutions
            for t in self._generate_tbuf_fromsum(tbuf[:], sum-c, offset+1, c):
                yield t


class RecursiveOptimized(Solver.Base.Base):  
    def __init__(self):
        super(RecursiveOptimized, self).__init__()
        self.callback = None
        self.hints['interval'] = (0xff, 0x00)
    
    def solve(self, callback=None):
        # temporary data buffer
        self.tbuf = bytearray([self.hints['interval'][1]]*self.hints['length'])
        self.callback = callback
        
        if self.hints['sum']==0:
            self._found_solution(tbuf)
        else:
            self._generate_tbuf_fromsum(self.hints['sum'], 0, self.hints['interval'][0])
        
        self.callback = None
        
    def _found_solution(self, tbuf, depth):
        return self.callback(tbuf, {
            'depth': depth
        })
        
    def _computeLimits(self, sum, offset, cc):
        return (
            None,
            min(self.hints['interval'][0], sum, cc), 
            self.hints['interval'][1]
        )
        
    def _generate_tbuf_fromsum(self, sum, offset, cc):
        if ((self.hints['length']-offset)*self.hints['interval'][0])<sum:
            #return 1+((sum - ((self.hints['length']-offset-1)*self.hints['interval'][0]))//self.hints['interval'][0])
            return CallbackResult(1+((sum - ((self.hints['length']-offset-1)*self.hints['interval'][0]))//self.hints['interval'][0]))

        """
            use either
                for c in range(min(self.hints['interval'][0], sum, cc), self.hints['interval'][1]-1, -1):
                    ....
            or
                c = min(self.hints['interval'][0], sum, cc)+1
                cmin = self.hints['interval'][1]
                while c > cmin:
                    c-=1
                    ....

        """
        
        (r, c, cmin) = self._computeLimits(sum, offset, cc)
        if r:
            if r.up>0:
                return CallbackResult(r.up-1, r.skipSibling)

        cmin-=1
        self.tbuf[offset] = cmin
        noffset = offset+1
        
        while c > cmin:
            self.tbuf[offset] = c
            nsum = sum-c
            if nsum==0:  # match found
                r = self._found_solution(self.tbuf, offset)
                if r:
                    if r.up>0:
                        return CallbackResult(r.up-1, r.skipSibling)
                        
                    if r.skipSibling>0:
                        c = max(c-r.skipSibling, cmin)
            else:
                if noffset<self.hints['length']:
                    # check childs
                    r = self._generate_tbuf_fromsum(nsum, noffset, c)
                    if r:
                        if r.up>0:
                            self.tbuf[offset] = self.hints['interval'][1]
                            return CallbackResult(r.up-1, r.skipSibling)
                            
                        if r.skipSibling>0:
                            c = max(c-r.skipSibling, cmin)
                else:
                    break
            c-=1
        self.tbuf[offset] = self.hints['interval'][1] # not sure this is needed
        return None
