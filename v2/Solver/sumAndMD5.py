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
    
    def solve(self):
        slv = Solver.sum.V1()
        slv.setHint('length', self.hints['length'])
        slv.setHint('sum', self.hints['sum'])
    
        for tbuf in slv.solve():
            # step1: calculate permutations
            for tpbuf in itertools.permutations(tbuf):
                # step2: for each permutation, check the md5 hash
                h = hashlib.md5()
                h.update(bytes(tpbuf))
                if h.hexdigest()==self.hints['md5']:
                    print("found")
                    self.print_tbuf(tpbuf)
                    self.print_buf_as_str(tpbuf)
                    yield tpbuf
            
            
        print("not found")
        
            
        
    