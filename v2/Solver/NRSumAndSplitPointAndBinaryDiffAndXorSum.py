# -*- coding: utf-8 -*-
import sys, time

import Solver.Base
from Solver.Base import CallbackResult

class V1(Solver.Base.Base):
    def __init__(self):
        # general vars
        self.callback = None
        self.stats = {}
        self.hints = {}
        
        # internals
        self._stack = []
        self._precalc_binaryDiffRSums = []
        self._precalc_binaryDiffRSumsV2 = []
        self._precalc_returns = []
        self._precalc__computeLimits = []
        
        self._precalc__computeLimits_lt = 0
        self._precalc__computeLimits_gt = 0
        
        self.hints['length'] = None # the length of the output data
        self.hints['sum'] = None    # the sum of the output data
        self.hints['md5'] = None    # the md5 sum of the output data
        self.hints['interval'] = (0xff, 0x00)
        self.hints['value'] = None
        self.hints['index'] = None
        self.hints['binarydiff'] = ()
        self.hints['xorsum'] = 0x00
        self.hints['finalValues'] = ()
        
    def initialize(self):
        if len(self.hints['finalValues'])==0:
            self.hints['finalValues'] = [None]*self.hints['length']
            
            
        for (offset, _) in enumerate(self.hints['binarydiff']):
            # binaryDiffs
            self._precalc_binaryDiffRSums.append(sum(self.hints['binarydiff'][offset:]))
            self._precalc_binaryDiffRSumsV2.append(sum(self.hints['binarydiff'][offset+1:]))


        for offset in range(self.hints['length']):
            # _stack
            self._stack.append(None)
            
            # _precalc__computeLimits
            pc = None
            if pc is None and not self.hints['finalValues'][offset] is None:
                pc = (
                    self.hints['finalValues'][offset][0],
                    self.hints['finalValues'][offset][1] - 1
                )
                
            if pc is None and offset==self.hints['index']:
                pc = (
                    self.hints['value'],
                    self.hints['value'] - 1
                )
            if pc is None:
                if (self._precalc_binaryDiffRSumsV2[offset]==self._precalc_binaryDiffRSumsV2[self.hints['length']-1]):
                    pc = (
                        self.hints['interval'][1],
                        self.hints['interval'][1] - 1
                    )        
                elif (self._precalc_binaryDiffRSumsV2[offset]==self._precalc_binaryDiffRSumsV2[self.hints['index']]):
                    pc = (
                        self.hints['value'],
                        self.hints['value'] - 1
                    )
                elif (self._precalc_binaryDiffRSumsV2[offset]==self._precalc_binaryDiffRSumsV2[0]):
                    pc = (
                        self.hints['interval'][0],
                        self.hints['interval'][0] - 1
                    )
                
            self._precalc__computeLimits.append(pc)
            
            # _precalc_returns
            i = offset
            #while self._precalc_binaryDiffRSumsV2[i]==self._precalc_binaryDiffRSumsV2[offset]:
            while self._precalc_binaryDiffRSums[i]==self._precalc_binaryDiffRSums[offset]:
                i-=1
            self._precalc_returns.append((offset-i) + 2)
        
        
        self._precalc__computeLimits_lt = self.hints['value'] - self._precalc_binaryDiffRSumsV2[self.hints['index']] - 1
        self._precalc__computeLimits_gt = self.hints['interval'][1] - 1
        
        s = ""
        for d in self._precalc__computeLimits:
            if d is None:
                s+= "None, " 
            else:
                s+= "0x%02x-0x%02x, " % (d[0], d[1]+1)
        print("(%s)" % (s))
            
    def _found_solution(self, tbuf):
        # DEBUGGING
        #sys.stdout.write("\n ##### '%s' sum:%d (%s)" % (self.print_buf_as_str(self.tbuf), self.print_buf_as_sum(self.tbuf), self.print_buf_as_binarydiff(tbuf)))
        #sys.stdout.flush()
        
        # DEBUGGING
        #self.stats['_generate_tbuf_fromsum::reports']-=1
        #if self.stats['_generate_tbuf_fromsum::reports']<0:
        #    sys.stdout.write("\n %s (%s)" % (self.print_buf_as_str(self.tbuf), self.print_buf_as_binarydiff(tbuf)))
        #    sys.stdout.flush()
        #    self.stats['_generate_tbuf_fromsum::reports']=self.stats['_generate_tbuf_fromsum::maxReports']
            
        return self.callback(tbuf, { })
        
    def _computeLimits(self, offset, cc):
        if self._precalc__computeLimits[offset]:
            return self._precalc__computeLimits[offset]
        else:
            if self.hints['binarydiff'][offset]==0:
                return (
                    cc,
                    cc - 1
                )
            elif self.hints['binarydiff'][offset]==1:
                if offset<self.hints['index']:
                    return (
                        cc - 1,
                        self._precalc__computeLimits_lt + self._precalc_binaryDiffRSumsV2[offset]
                    )
                else:
                    return (
                        cc - 1,
                        self._precalc__computeLimits_gt + self._precalc_binaryDiffRSumsV2[offset]
                    )

    def solve(self, callback=None):
        self.callback = callback
        self.solve_lin(callback)
        self.callback = None
    

    def solve_lin(self, callback=None):
        # temporary data buffer
        self.tbuf = bytearray([self.hints['interval'][1]]*self.hints['length'])
        
        offset = 0
        
        (cmax, cmin) = self._computeLimits(offset, self.hints['interval'][0])
        self._stack[0] = [
            self.hints['interval'][0], 
            self.hints['sum'], 
            self.hints['xorsum'], 
            cmax, 
            cmin,
        ]
        
        doContinue = True
       
        while True:
            #0,   1,      2,    3,    4, 
            (c, sum, xorsum, cmax, cmin, ) = self._stack[offset]
            
            doContinue = False
            while c > cmin:
                self.tbuf[offset] = c
                nsum = sum - c
                nxorsum = xorsum ^ c
                
                #print("%s 0x%02x (%c)" % ("  "*offset, c, c))
                #print("%s %c" % ("  "*offset, c))
                
                if offset==(self.hints['length']-2): # -2 instead of -1 is an optimization, because we already know the last element in the list, we can avoid an extra depth-walk
                    if nsum == self.hints['interval'][1]:
                        if nxorsum == self.hints['interval'][1]:
                            r = self._found_solution(self.tbuf)
                            offset-= self._precalc_returns[offset]
                            #offset-= 1
                            break
                else:                        # noffset<(self.hints['length']-1):, still something to distribuite
                    # check childs
                    doContinue = True
                    self._stack[offset][0] = c-1
                    
                    # push to stack
                    offset+=1
                    (ncmax, ncmin) = self._computeLimits(offset, c)
                    
                    self._stack[offset] = [
                        ncmax, 
                        nsum, 
                        nxorsum, 
                        ncmax, 
                        ncmin, 
                    ]
                    break   # break while c>cmin
                c-=1
            # end of while c>cmin
            
            
            if doContinue==False:   # pop the stack
                #print("%d returns %d" % (offset, precalc_ret-1))
                #offset-= precalc_ret-1 # why isn't this working?
                offset-= 1
                
                if offset<0:
                    break # stop the main loop
            
            