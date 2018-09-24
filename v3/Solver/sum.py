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
        self.hints['altsum'] = 0
        
        self.stats['_generate_tbuf_fromsum:found'] = 0
        self.stats['_generate_tbuf_fromsum:calls'] = 0
        self.stats['_generate_tbuf_fromsum:misses:overflow'] = 0
    
    def solve(self):
        # temporary data buffer
        tbuf = bytearray([0]*self.hints['length'])
        for t in self._generate_tbuf_fromsum(tbuf[:], self.hints['altsum'], 0, 0xff, 0x00):
            yield t
    
    def _generate_tbuf_fromsum(self, tbuf, altsum, offset, cc, xor):
        self.stats['_generate_tbuf_fromsum:calls']+= 1
        if altsum==0 and xor==self.hints['xor'] and offset==(self.hints['length']+1):
            self.stats['_generate_tbuf_fromsum:found']+= 1
            #self.print_tbuf(tbuf)
            yield tbuf
            
        if offset>=self.hints['length']:
            self.stats['_generate_tbuf_fromsum:misses:overflow']+= 1
            return
        
        for c in range(cc, 0x00, -1):
            tbuf[offset] = c
            self.print_tbuf(tbuf)
            
            # propagate found solutions
            if offset % 2==0:
                nsum = altsum + c
            else:
                nsum = altsum - c
                
            for t in self._generate_tbuf_fromsum(tbuf[:], nsum, offset+1, c, xor ^ c):
                yield t

