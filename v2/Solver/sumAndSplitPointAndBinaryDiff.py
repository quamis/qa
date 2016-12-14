# -*- coding: utf-8 -*-
import Solver.Base
import Solver.sum
import Solver.sumAndSplitPoint
from Solver.Base import CallbackResult


"""
    doesn't seem to optimize that much
    not sure why in some cases it actually skips valid results
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
        
    def _computeLimits(self, sum, offset, cc):
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
                    min(self.hints['interval'][0], sum, cc) - self.hints['binarydiff'][offset], 
                    min(self.hints['interval'][0], sum, cc) - self.hints['binarydiff'][offset]
                )
            else:
                return(
                    None,
                    min(self.hints['interval'][0], sum, cc) - self.hints['binarydiff'][offset], 
                    self.hints['value']
                )
            
        elif self.indexMap[offset]==0x7:
            if self.hints['binarydiff'][offset]==0:
                return(
                    None,
                    min(self.hints['interval'][0], sum, cc) - self.hints['binarydiff'][offset], 
                    min(self.hints['interval'][0], sum, cc) - self.hints['binarydiff'][offset]
                )
            else:
                return(
                    None,
                    min(self.hints['interval'][0], sum, cc) - self.hints['binarydiff'][offset], 
                    self.hints['value']
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
                    min(self.hints['value']-1, sum, cc) - self.hints['binarydiff'][offset],
                    min(self.hints['value']-1, sum, cc) - self.hints['binarydiff'][offset]
                )

            else:
                return(
                    None,
                    min(self.hints['value']-1, sum, cc) - self.hints['binarydiff'][offset],
                    self.hints['interval'][1]
                )
            
        elif self.indexMap[offset]==0xa:
            if self.hints['binarydiff'][offset]==0:
                return(
                    None,
                    min(self.hints['value']-1, sum, cc) - self.hints['binarydiff'][offset],
                    min(self.hints['value']-1, sum, cc) - self.hints['binarydiff'][offset]
                )
            else:
                return(
                    None,
                    min(self.hints['value']-1, sum, cc) - self.hints['binarydiff'][offset],
                    self.hints['interval'][1]
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
        
        nsumoffset = (self.hints['length'] - noffset)*self.hints['interval'][1]
        
        self.stats['_generate_tbuf_fromsum::reports']-=1
        
        while c > cmin:
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
