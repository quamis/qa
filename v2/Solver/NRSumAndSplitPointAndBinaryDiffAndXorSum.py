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
        self.indexMap = None
        self.binaryDiffRSums = []
        self.binaryDiffRSumsV2 = []
        
        self.hints['length'] = None # the length of the output data
        self.hints['sum'] = None    # the sum of the output data
        self.hints['md5'] = None    # the md5 sum of the output data
        self.hints['interval'] = (0xff, 0x00)
        self.hints['value'] = None
        self.hints['index'] = None
        self.hints['binarydiff'] = ()
        self.hints['xorsum'] = 0x00
        self.hints['finalValues'] = ()
        
        
        self.stats['_found_solution'] = {}
        self.stats['_found_solution']['calls'] = 0
        self.stats['_computeLimits'] = {}
        self.stats['_computeLimits']['o==i'] = 0
        self.stats['_computeLimits']['dro==drl'] = 0
        self.stats['_computeLimits']['dro==i'] = 0
        self.stats['_computeLimits']['dro==0'] = 0
        self.stats['_computeLimits']['bdo==0'] = 0
        self.stats['_computeLimits']['bdo==1, o<i'] = 0
        self.stats['_computeLimits']['bdo==1, o>=i'] = 0
        self.stats['_computeLimits']['precalc'] = 0
        self.stats['_generate_tbuf_fromsum::maxReports'] = 2000
        self.stats['_generate_tbuf_fromsum::reports'] = self.stats['_generate_tbuf_fromsum::maxReports']
        
        self.stats['_generate_tbuf_fromsum::printIntervalMax'] = 100000
        self.stats['_generate_tbuf_fromsum::printInterval'] = self.stats['_generate_tbuf_fromsum::printIntervalMax']
        self.stats['solve_lin']={}
        self.stats['solve_lin']['ret:sum+xor:True'] = 0
        self.stats['solve_lin']['ret:sum+xor:False'] = 0
        self.stats['solve_lin']['go:deep'] = 0
        self.stats['solve_lin']['iter:depth'] = {}
        
        
    def initialize(self):
        for (offset, v) in enumerate(self.hints['binarydiff']):
            self.binaryDiffRSums.append(sum(self.hints['binarydiff'][offset:]))
            self.binaryDiffRSumsV2.append(sum(self.hints['binarydiff'][offset+1:]))
            
        if len(self.hints['finalValues'])==0:
            self.hints['finalValues'] = [None]*self.hints['length']
            
        for offset in range(self.hints['length']):
            self.stats['solve_lin']['iter:depth'][offset] = 0
            
        self._precalc__computeLimits = []
        for offset in range(self.hints['length']):
            pc = None
            if pc is None and not self.hints['finalValues'][offset] is None:
                pc = (
                    self.hints['finalValues'][offset][0],
                    self.hints['finalValues'][offset][1],
                )
                
            if pc is None and offset==self.hints['index']:
                self.stats['_computeLimits']['o==i']+= 1
                pc = (
                    self.hints['value'],
                    self.hints['value']
                )
            if pc is None:
                if (self.binaryDiffRSumsV2[offset]==self.binaryDiffRSumsV2[self.hints['length']-1]):
                    self.stats['_computeLimits']['dro==drl']+= 1
                    pc = (
                        self.hints['interval'][1],
                        self.hints['interval'][1]
                    )        
                elif (self.binaryDiffRSumsV2[offset]==self.binaryDiffRSumsV2[self.hints['index']]):
                    self.stats['_computeLimits']['dro==i']+= 1
                    pc = (
                        self.hints['value'],
                        self.hints['value']
                    )
                elif (self.binaryDiffRSumsV2[offset]==self.binaryDiffRSumsV2[0]):
                    self.stats['_computeLimits']['dro==0']+= 1
                    pc = (
                        self.hints['interval'][0],
                        self.hints['interval'][0]
                    )
                
            self._precalc__computeLimits.append(pc)
        
        
    def _found_solution(self, tbuf):
        self.stats['_found_solution']['calls']+=1
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
            self.stats['_computeLimits']['precalc']+= 1
            return self._precalc__computeLimits[offset]
        else:
            if self.hints['binarydiff'][offset]==0:
                self.stats['_computeLimits']['bdo==0']+= 1
                return (
                    cc,
                    cc
                )
            elif self.hints['binarydiff'][offset]==1:
                if offset<self.hints['index']:
                    self.stats['_computeLimits']['bdo==1, o<i']+= 1
                    return (
                        cc - 1,
                        self.hints['value'] + (self.binaryDiffRSumsV2[offset] - self.binaryDiffRSumsV2[self.hints['index']])
                    )
                else:
                    self.stats['_computeLimits']['bdo==1, o>=i']+= 1
                    return (
                        cc - 1,
                        (self.hints['interval'][1] + self.binaryDiffRSumsV2[offset])    # equivalent to (self.hints['interval'][1] + sum(self.hints['binarydiff'][offset+1:])) 
                    )

    """
    def _computeLimits(self, offset, cc):
        if not self.hints['finalValues'][offset] is None:
            return (
                self.hints['finalValues'][offset][0],
                self.hints['finalValues'][offset][1],
            );
    
        if offset==self.hints['index']:
            self.stats['_computeLimits']['o==i']+= 1
            return (
                self.hints['value'],
                self.hints['value']
            )

        # the order of the if's apparently matters
        if (self.binaryDiffRSumsV2[offset]==self.binaryDiffRSumsV2[self.hints['length']-1]):
            self.stats['_computeLimits']['dro==drl']+= 1
            return (
                self.hints['interval'][1],
                self.hints['interval'][1]
            )        
        elif (self.binaryDiffRSumsV2[offset]==self.binaryDiffRSumsV2[self.hints['index']]):
            self.stats['_computeLimits']['dro==i']+= 1
            return (
                self.hints['value'],
                self.hints['value']
            )
        elif (self.binaryDiffRSumsV2[offset]==self.binaryDiffRSumsV2[0]):
            self.stats['_computeLimits']['dro==0']+= 1
            return (
                self.hints['interval'][0],
                self.hints['interval'][0]
            )

        
        if self.hints['binarydiff'][offset]==0:
            self.stats['_computeLimits']['bdo==0']+= 1
            return (
                cc,
                cc
            )
        elif self.hints['binarydiff'][offset]==1:
            if offset<self.hints['index']:
                self.stats['_computeLimits']['bdo==1, o<i']+= 1
                return (
                    cc - 1,
                    self.hints['value'] + (self.binaryDiffRSumsV2[offset] - self.binaryDiffRSumsV2[self.hints['index']])
                )
            else:
                self.stats['_computeLimits']['bdo==1, o>=i']+= 1
                return (
                    cc - 1,
                    (self.hints['interval'][1] + self.binaryDiffRSumsV2[offset])    # equivalent to (self.hints['interval'][1] + sum(self.hints['binarydiff'][offset+1:])) 
                )
    """
    
    def solve(self, callback=None):
        self.callback = callback
        self.solve_lin(callback)
        self.callback = None
    

    def solve_lin(self, callback=None):
        # temporary data buffer
        self.tbuf = bytearray([self.hints['interval'][1]]*self.hints['length'])
        
        self._stack = []
        for offset in range(self.hints['length']):
            i = offset
            #while self.binaryDiffRSumsV2[i]==self.binaryDiffRSumsV2[offset]:
            while self.binaryDiffRSums[i]==self.binaryDiffRSums[offset]:
                i-=1
            precalc_ret = (offset-i) + 1
            #print(precalc_ret)
            self._stack.append([
                None, 
                None, 
                None, 
                None, 
                None, 
                (self.hints['length'] - offset - 1)*self.hints['interval'][1],
                precalc_ret,
                ])
        
        offset = 0
        
        (cmax, cmin) = self._computeLimits(offset, self.hints['interval'][0])
        self._stack[0] = [
            self.hints['interval'][0], 
            self.hints['sum'], 
            self.hints['xorsum'], 
            cmax, 
            cmin-1,
            self._stack[0][5],
            self._stack[0][6],
        ]
        
        doContinue = True
       
        while True:
            #0,   1,      2,    3,    4,          5,           6
            (c, sum, xorsum, cmax, cmin, nsumoffset, precalc_ret) = self._stack[offset]
            
            doContinue = False
            while c > cmin:
                self.tbuf[offset] = c
                nsum = sum - c
                nxorsum = xorsum ^ c
                
                self.stats['solve_lin']['iter:depth'][offset]+=1
                
                if offset==(self.hints['length']-2): # -2 instead of -1 is an optimization, because we already know the last element in the list, we can avoid an extra depth-walk
                    if (nsum - nsumoffset)==0:
                        if nxorsum == self.hints['interval'][1]:
                            self.stats['solve_lin']['ret:sum+xor:True']+=1
                            r = self._found_solution(self.tbuf)

                            offset-=precalc_ret
                            break
                        else:
                            self.stats['solve_lin']['ret:sum+xor:False']+=1
                            
                            offset-=precalc_ret
                            break
                else:                        # noffset<(self.hints['length']-1):, still something to distribuite
                    # check childs
                    
                    self.stats['solve_lin']['go:deep']+=1
                    doContinue = True
                    self._stack[offset][0] = c-1
                    offset+=1
                    (ncmax, ncmin) = self._computeLimits(offset, c)
                    
                    # push to stack
                    self._stack[offset] = [
                        ncmax, 
                        nsum, 
                        nxorsum, 
                        ncmax, 
                        ncmin-1, 
                        self._stack[offset][5],
                        self._stack[offset][6],
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
            
            