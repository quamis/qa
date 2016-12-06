# -*- coding: utf-8 -*-
import sys, time, hashlib, zlib, statistics

import itertools
import Solver.Base
import Solver.sum

"""
    seems accurate, fast, 0 false-positives
    non-recursive
"""
class V1(Solver.Base.Base):
    def __init__(self):
        super(V1, self).__init__()
        self.callback = None
    
    def solve(self, callback=None):
        slv = Solver.sum.V1_3()
        slv.setHint('length', self.hints['length'])
        slv.setHint('sum', self.hints['sum'])
        
        self.callback = callback
        slv.solve(callback=self._evt_sum_solved)
        self.callback = None
        

    def _evt_sum_solved(self, buf, depth):
        md = int(statistics.median(buf))
        
        """
        if self.hints['median']==md:
            sys.stdout.write("\n%s median:0x%02x ==\n" % (self.print_tbuf(buf), md))
        
        if self.hints['median']-5>md:
            sys.stdout.write("\r%s median:0x%02x >...%d" % (self.print_tbuf(buf), md, int(max(0, depth - 6/2))))
            return {'return': max(0, depth - 6/2)}
        elif self.hints['median']+1<md:
            sys.stdout.write("\r%s median:0x%02x <" % (self.print_tbuf(buf), md))
            return {'return': max(0, depth-1)}
            
        sys.stdout.write("\r%s median:0x%02x =" % (self.print_tbuf(buf), md))
        """
        
        if self.hints['median']==md:
            sys.stdout.write("\r\n%s median:0x%02x ==\n\r" % (self.print_tbuf(buf), md))
        else:
            if md>self.hints['median']:
                sys.stdout.write("\r%s median:0x%02x > (d:%d)" % (self.print_tbuf(buf), md, depth))
                return {'return': min(self.hints['length']/2, depth-1)-3}
            elif md<self.hints['median']:
                sys.stdout.write("\r%s median:0x%02x < (d:%d)" % (self.print_tbuf(buf), md, depth))
                return {'return': min(self.hints['length']/2, depth-1)-3}
            else:
                sys.stdout.write("\r%s median:0x%02x = (d:%d)" % (self.print_tbuf(buf), md, depth))
            
