# -*- coding: utf-8 -*-
import sys

import Solver.Base
import Solver.sum
import Solver.sumAndSplitPoint
from Solver.Base import CallbackResult


"""
    this class still generates false data, instead of 0100 it will still generate 0110 or something like that. I'm not sure why
    
    this should be further optimized, a completly different approach to resolving the input data can be approched by havning the relationships between elements
    
"""
class V1(Solver.sumAndSplitPoint.Optimized):
    def __init__(self):
        super(V1, self).__init__()
        self.callback = None
        self.hints['binarydiff'] = ()
        
    def solve(self, callback=None):
        # temporary data buffer
        self.tbuf = bytearray([self.hints['interval'][1]]*self.hints['length'])
        self.callback = callback
        
        if self.hints['sum']==0:
            self._found_solution(tbuf)
        else:
            #self._generate_tbuf_fromsum(self.hints['sum'] - (self.hints['interval'][1]*self.hints['length']), 0, self.hints['interval'][0])
            self._generate_tbuf_fromsum(self.hints['sum'], 0, self.hints['interval'][0])
        
        self.callback = None
        
    def _computeLimits(self, tsum, offset, cc):
        self.stats['_computeLimits'][self.indexMap[offset]]+=1
        
        if    self.indexMap[offset]==0x1:
            return(
                None,
                self.hints['interval'][0],
                self.hints['interval'][0]
            )
        elif self.indexMap[offset]==0x6:
            if self.hints['binarydiff'][offset]==0:
                return(
                    None,
                    cc, 
                    cc
                )
            else:
                return(
                    None,
                    min(self.hints['interval'][0], tsum, cc) - self.hints['binarydiff'][offset], 
                    self.hints['value'] + sum(self.hints['binarydiff'][offset:(self.hints['index'] - offset)]),
                )
            
        elif self.indexMap[offset]==0x7:
            if self.hints['binarydiff'][offset]==0:
                return(
                    None,
                    cc, 
                    cc
                )
            else:
                return(
                    None,
                    min(self.hints['interval'][0], tsum, cc) - self.hints['binarydiff'][offset], 
                    self.hints['value'] + sum(self.hints['binarydiff'][offset:(self.hints['index'] - offset)]),
                )
            
        elif self.indexMap[offset]==0x8:
            return(
                None,
                self.hints['value'],
                self.hints['value']
            )
            
        elif self.indexMap[offset]==0x9:   
            if self.hints['binarydiff'][offset]==0:
                return(
                    None,
                    cc,
                    cc
                )

            else:
                return(
                    None,
                    min(self.hints['value']-1, tsum, cc) - self.hints['binarydiff'][offset],
                    self.hints['interval'][1] + sum(self.hints['binarydiff'][offset:])
                )
            
        elif self.indexMap[offset]==0xa:
            if self.hints['binarydiff'][offset]==0:
                return(
                    None,
                    cc,
                    cc
                )
            else:
                return(
                    None,
                    min(self.hints['value']-1, tsum, cc) - self.hints['binarydiff'][offset],
                    self.hints['interval'][1] + sum(self.hints['binarydiff'][offset:])
                )
            
        elif self.indexMap[offset]==0xf:
            return(
                None,
                self.hints['interval'][1],
                self.hints['interval'][1]
            )
        
    def _generate_tbuf_fromsum(self, sum, offset, cc):
        #if ((self.hints['length']-offset)*self.hints['interval'][0])<sum:
            #return 1+((sum - ((self.hints['length']-offset-1)*self.hints['interval'][0]))//self.hints['interval'][0])
        #    return CallbackResult(1+((sum - ((self.hints['length']-offset-1)*self.hints['interval'][0]))//self.hints['interval'][0]))
        
        # optimization. this might induce too many skipped steps, but it seems to work ok for now
        if ((self.hints['length'] - offset)*cc)<sum:
            return CallbackResult(0)
            
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
        
        # did binary check failed?
        #if offset>2 and (self.hints['binarydiff'][offset-1]==0 and self.hints['binarydiff'][offset-2]==0) and (self.tbuf[offset-1]!=self.tbuf[offset-2]):  
        #    return CallbackResult(3)
            
        nsumoffset = (self.hints['length'] - noffset)*self.hints['interval'][1]
        
        self.stats['_generate_tbuf_fromsum::reports']-=1
        
        while c > cmin:
            # did binary check failed?
            #if offset>2 and (self.hints['binarydiff'][offset]==0 and self.hints['binarydiff'][offset-1]==0) and (self.tbuf[offset-1]!=c):
            #    #c-=1
            #    #continue
            #    break
                
            #if offset>8 and (self.hints['binarydiff'][offset]==0 and self.hints['binarydiff'][offset-1]==1) and (self.tbuf[offset-1]!=c):
            #    c-=1
            #    continue
            #    #break
            #    #pass
            
            #if offset>2 and (self.hints['binarydiff'][offset]==1 and self.hints['binarydiff'][offset-1]==1) and (self.tbuf[offset-1]==c):
            #    c-=1
            #    continue
            #    break
            #    #break
            #    #pass
            #    exit()
            #    self.tbuf[offset] = self.hints['interval'][1] # not sure this is needed
            #    return CallbackResult(2)
        
            self.tbuf[offset] = c
            nsum = sum - c
            
            if (nsum - nsumoffset)==0:  # match found
                r = self._found_solution(self.tbuf, offset)
                if r:
                    if r.up>0:
                        self.tbuf[offset] = self.hints['interval'][1] # not sure this is needed
                        return CallbackResult(r.up-1, r.skipSibling)
                        
                    if r.skipSibling>0:
                        c = max(c-r.skipSibling, cmin)
            elif (nsum - nsumoffset)<0:  # overshoot
                # do nothing, skip one step
                pass   
            else:                        # still something to distribuite
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


class V2(Solver.Base.Base):  
    def __init__(self):
        super(V2, self).__init__()
        self.callback = None
        self.hints['interval'] = (0xff, 0x00)
        self.hints['value'] = None
        self.hints['index'] = None
        self.hints['binarydiff'] = ()
        self.hints['finalValues'] = ()
        
        self.indexMap = None
        self.binaryDiffRSums = []
        self.binaryDiffRSumsV2 = []
        
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
        
    
    def solve(self, callback=None):
        # temporary data buffer
        self.tbuf = bytearray([self.hints['interval'][1]]*self.hints['length'])
        self.callback = callback
        
        if self.hints['sum']==0:
            self._found_solution(tbuf)
        else:
            #self._generate_tbuf_fromsum(self.hints['sum'] - (self.hints['interval'][1]*self.hints['length']), 0, self.hints['interval'][0])
            self._generate_tbuf_fromsum(self.hints['sum'], 0, self.hints['interval'][0])
        
        self.callback = None
    
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
                
    def _generate_tbuf_fromsum(self, sum, offset, cc):
        noffset = offset+1
        nsumoffset = (self.hints['length'] - noffset)*self.hints['interval'][1]
        
        # optimization
        # thse checks should be done after _computeLimits? or even taken into consideration in _computeLimits?
        if ((self.hints['length'] - offset)*self.hints['interval'][1])>(sum):
            return 0
            
        (r, c, cmin) = self._computeLimits(offset, cc)
        if r:
            return r-1
        
        
        if cc<cmin:
            exit()

        cmin-= 1
        
        ret = 0
        while c > cmin:
            self.tbuf[offset] = c
            nsum = sum - c
            
            if noffset==(self.hints['length']-1):
                if (nsum - nsumoffset)==0:
                    r = self._found_solution(self.tbuf)
                    if r:
                        ret = r-1
                        break
            else:                        # noffset<(self.hints['length']-1):, still something to distribuite
                # check childs
                r = self._generate_tbuf_fromsum(nsum, noffset, c)
                if r:
                    ret = r-1
                    break
            c-=1
        
        self.tbuf[offset] = self.hints['interval'][1] # not sure this is needed
        return ret

    """
    def _generate_tbuf_fromsum_reversed(self, sum, offset, cc):
        noffset = offset+1
        nsumoffset = (self.hints['length'] - noffset)*self.hints['interval'][1]
        
        # optimization
        # thse checks should be done after _computeLimits? or even taken into consideration in _computeLimits?
        if ((self.hints['length'] - offset)*self.hints['interval'][1])>(sum):
            return 0
            
        (r, c, cmin) = self._computeLimits(offset, cc)
        if r:
            return r-1
        
        if noffset>self.hints['index']:
            cmax = c+1
            c = cmin
            
            ret = 0
            while c < cmax:
                self.tbuf[offset] = c
                nsum = sum - c
                
                if noffset==(self.hints['length']-1):
                    if (nsum - nsumoffset)==0:
                        r = self._found_solution(self.tbuf)
                        if r:
                            ret = r-1
                            break
                else:                        # noffset<(self.hints['length']-1):, still something to distribuite
                    # check childs
                    r = self._generate_tbuf_fromsum(nsum, noffset, c)
                    if r:
                        ret = r-1
                        break
                c+=1
        else:
            cmin-= 1
            
            ret = 0
            while c > cmin:
                self.tbuf[offset] = c
                nsum = sum - c
                
                if noffset==(self.hints['length']-1):
                    if (nsum - nsumoffset)==0:
                        r = self._found_solution(self.tbuf)
                        if r:
                            ret = r-1
                            break
                else:                        # noffset<(self.hints['length']-1):, still something to distribuite
                    # check childs
                    r = self._generate_tbuf_fromsum(nsum, noffset, c)
                    if r:
                        ret = r-1
                        break
                c-=1
        
        self.tbuf[offset] = self.hints['interval'][1] # not sure this is needed
        return ret
    """