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
        self.stats['_generate_tbuf_fromsum::maxReports'] = 2000
        self.stats['_generate_tbuf_fromsum::reports'] = self.stats['_generate_tbuf_fromsum::maxReports']
        
        self.stats['_generate_tbuf_fromsum::printIntervalMax'] = 100000
        self.stats['_generate_tbuf_fromsum::printInterval'] = self.stats['_generate_tbuf_fromsum::printIntervalMax']
        
        
    def initialize(self):
        for (offset, v) in enumerate(self.hints['binarydiff']):
            self.binaryDiffRSums.append(sum(self.hints['binarydiff'][offset:]))
            self.binaryDiffRSumsV2.append(sum(self.hints['binarydiff'][offset+1:]))
            
        if len(self.hints['finalValues'])==0:
            self.hints['finalValues'] = [None]*self.hints['length']
        
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
        if not self.hints['finalValues'][offset] is None:
            return (
                None,
                self.hints['finalValues'][offset][0],
                self.hints['finalValues'][offset][1],
            );
    
        if offset==self.hints['index']:
            self.stats['_computeLimits']['o==i']+= 1
            return (
                None,
                self.hints['value'],
                self.hints['value']
            )

        # the order of the if's apparently matters
        if (self.binaryDiffRSumsV2[offset]==self.binaryDiffRSumsV2[self.hints['length']-1]):
            self.stats['_computeLimits']['dro==drl']+= 1
            return (
                None,
                self.hints['interval'][1],
                self.hints['interval'][1]
            )        
        elif (self.binaryDiffRSumsV2[offset]==self.binaryDiffRSumsV2[self.hints['index']]):
            self.stats['_computeLimits']['dro==i']+= 1
            return (
                None,
                self.hints['value'],
                self.hints['value']
            )
        elif (self.binaryDiffRSumsV2[offset]==self.binaryDiffRSumsV2[0]):
            self.stats['_computeLimits']['dro==0']+= 1
            return (
                None,
                self.hints['interval'][0],
                self.hints['interval'][0]
            )

        
        if self.hints['binarydiff'][offset]==0:
            self.stats['_computeLimits']['bdo==0']+= 1
            return (
                None,
                cc,
                cc
            )
        elif self.hints['binarydiff'][offset]==1:
            if offset<self.hints['index']:
                self.stats['_computeLimits']['bdo==1, o<i']+= 1
                return (
                    None,
                    cc - 1,
                    self.hints['value'] + (self.binaryDiffRSumsV2[offset] - self.binaryDiffRSumsV2[self.hints['index']])
                )
            else:
                self.stats['_computeLimits']['bdo==1, o>=i']+= 1
                return (
                    None,
                    cc - 1,
                    (self.hints['interval'][1] + self.binaryDiffRSumsV2[offset])    # equivalent to (self.hints['interval'][1] + sum(self.hints['binarydiff'][offset+1:])) 
                )
                
    def solve_rec(self, callback=None):
        # temporary data buffer
        self.tbuf = bytearray([self.hints['interval'][1]]*self.hints['length'])
        self.callback = callback
        
        if self.hints['sum']==0:
            self._found_solution(bytearray([0]*self.hints['length']))
        else:
            #self._generate_tbuf_fromsum(self.hints['sum'] - (self.hints['interval'][1]*self.hints['length']), 0, self.hints['interval'][0])
            self._generate_tbuf_fromsum(self.hints['sum'], 0, self.hints['interval'][0], self.hints['xorsum'])
        
        self.callback = None
        
    def _generate_tbuf_fromsum(self, sum, offset, cc, xorsum):
        noffset = offset+1
        nsumoffset = (self.hints['length'] - noffset)*self.hints['interval'][1]
        
        # optimization
        # thse checks should be done after _computeLimits? or even taken into consideration in _computeLimits?
        if ((self.hints['length'] - offset)*self.hints['interval'][1])>(sum):
            return 0
            
        (r, c, cmin) = self._computeLimits(offset, cc)
        if r:
            return r-1
        
        cmin-= 1

        self.stats['_generate_tbuf_fromsum::printInterval']-=1
        if self.stats['_generate_tbuf_fromsum::printInterval']<0:
            sys.stdout.write("\n ~~~~~ '%s' sum:%d (%s)" % (self.print_buf_as_str(self.tbuf), self.print_buf_as_sum(self.tbuf), self.print_buf_as_binarydiff(self.tbuf)))
            sys.stdout.flush()
            self.stats['_generate_tbuf_fromsum::printInterval'] = self.stats['_generate_tbuf_fromsum::printIntervalMax']
        
        ret = 0
        while c > cmin:
            self.tbuf[offset] = c
            nsum = sum - c
            nxorsum = xorsum ^ c
            
            if noffset==(self.hints['length']-1):
                if (nsum - nsumoffset)==0:
                    if nxorsum == self.hints['interval'][1]:
                        r = self._found_solution(self.tbuf)
                        if r:
                            ret = r-1
                            break
                    else:
                        #ret = 4
                        break
            else:                        # noffset<(self.hints['length']-1):, still something to distribuite
                # check childs
                r = self._generate_tbuf_fromsum(nsum, noffset, c, nxorsum)
                if r:
                    ret = r-1
                    break
            c-=1
        
        self.tbuf[offset] = self.hints['interval'][1] # not sure this is needed
        return ret

    
    def solve(self, callback=None):
        self.callback = callback
        self.solve_lin(callback)
        self.callback = None
    

    def solve_lin(self, callback=None):
        # temporary data buffer
        self.tbuf = bytearray([self.hints['interval'][1]]*self.hints['length'])
        
        self._stack = []
        for i in range(self.hints['length']):
            self._stack.append([])
        
        offset = 0
        
        (r, cmax, cmin) = self._computeLimits(offset, self.hints['interval'][0])
        self._stack[offset] = [self.hints['interval'][0], self.hints['sum'], self.hints['xorsum'], cmax, cmin]
        
        doContinue = True
        
        while True:
            #print(offset)
            (c, sum, xorsum, cmax, cmin) = self._stack[offset]
            
            nsumoffset = (self.hints['length'] - offset + 1)*self.hints['interval'][1]
            
            doContinue = False
            cmin-= 1
            while c > cmin:
                
                self.tbuf[offset] = c
                nsum = sum - c
                nxorsum = xorsum ^ c
                
                if offset==(self.hints['length']-2):
                    if (nsum - nsumoffset)==0:
                        if nxorsum == self.hints['interval'][1]:
                            print("~~~~~ '%s' sum:%d" % (self.print_buf_as_str(self.tbuf), self.print_buf_as_sum(self.tbuf)))
                            r = self._found_solution(self.tbuf)
                            doContinue = False
                            break
                            # break????
                            
                    #        if r:
                    #            ret = r-1
                    #            break
                    #    else:
                    #        #ret = 4
                    #        break
                else:                        # noffset<(self.hints['length']-1):, still something to distribuite
                    # check childs
                    doContinue = True
                    self._stack[offset][0] = c-1
                    offset+=1
                    (r, ncmax, ncmin) = self._computeLimits(offset, c)
                    self._stack[offset] = [ncmax, nsum, nxorsum, ncmax, ncmin]
                    break   # break while c>cmin
                c-=1
            # old return?
            
            #self.tbuf[offset] = self.hints['interval'][1] # not sure this is needed
            # end of while c>cmin
            if doContinue==False:
                # pop the stack
                offset-=1
                if offset<0:
                    break # stop the main loop
                #(c, sum, xorsum, cmax, cmin) = self._stack[offset]
            
            