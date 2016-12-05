# -*- coding: utf-8 -*-
import sys, time, hashlib, zlib

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
        self.stats['_generate_tbuf_fromsum:found'] = 0
        self.callback = None
    
    def solve(self, callback=None):
        slv = Solver.sum.V1_3()
        slv.setHint('length', self.hints['length'])
        slv.setHint('sum', self.hints['sum'])
        
        self.callback = callback
        slv.solve(callback=self._evt_sum_solved)
        self.callback = None
        

    def _evt_sum_solved(self, buf):
        # step1: calculate permutations
        for tpbuf in itertools.permutations(buf):
            #print(self.print_tbuf(tpbuf))
            # step2: for each permutation, check the md5 hash
            h = hashlib.md5()
            h.update(bytes(tpbuf))
            if h.hexdigest()==self.hints['md5']:
                print("found")
                print(self.print_tbuf(tpbuf))
                print(self.print_buf_as_str(tpbuf))
                self.callback(tpbuf)
