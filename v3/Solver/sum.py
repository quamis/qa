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
        
        altsum = 0
        sum = 0
        xor = 0
        
        for c0 in range(0xff, 0x00, -1):
            tbuf[0] = c0
            sum+=c0
            altsum+= c0
            xor^= c0
            for c1 in range(c0, 0x00, -1):
                tbuf[1] = c1
                sum+=c1
                altsum-= c1
                xor^= c1
                for c2 in range(c1, 0x00, -1):
                    tbuf[2] = c2
                    sum+=c2
                    altsum+= c2
                    xor^= c2
                    for c3 in range(c2, 0x00, -1):
                        tbuf[3] = c3
                        sum+=c3
                        altsum-= c3
                        xor^= c3
                        
                        #if altsum==self.hints['altsum'] and xor==self.hints['xor'] and sum==0xc4:
                        if (altsum & 0x0f )==self.hints['altsum'] and (xor & 0x0f)==self.hints['xor']:
                            yield tbuf
                        
                        xor^= c3
                        altsum+= c3
                        sum-=c3
                    xor^= c2
                    altsum-= c2
                    sum-=c2
                xor^= c1
                altsum+= c1
                sum-=c1
            xor^= c0
            altsum-= c0
            sum-=c0