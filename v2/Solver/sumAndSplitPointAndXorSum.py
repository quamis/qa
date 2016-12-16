# -*- coding: utf-8 -*-
import Solver.Base
import Solver.sum
import Solver.sumAndSplitPoint
import Solver.sumAndSplitPointAndBinaryDiff
from Solver.Base import CallbackResult


"""
    doesn't seem to optimize that much
    not sure why in some cases it actually skips valid results
"""
class V1(Solver.sumAndSplitPoint.Optimized):
    def __init__(self):
        super(V1, self).__init__()
        self.callback = None
        self.hints['xorsum'] = 0x00
        
    def solve(self, callback=None):
        # temporary data buffer
        self.tbuf = bytearray([self.hints['interval'][1]]*self.hints['length'])
        self.callback = callback
        
        if self.hints['sum']==0:
            self._found_solution(tbuf)
        else:
            #self._generate_tbuf_fromsum(self.hints['sum'] - (self.hints['interval'][1]*self.hints['length']), 0, self.hints['interval'][0])
            self._generate_tbuf_fromsum(self.hints['sum'], 0, self.hints['interval'][0], 0x00)
        
        self.callback = None
        
    def _generate_tbuf_fromsum(self, sum, offset, cc, xorsum):
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
            nxorsum = xorsum ^ c
            nsum = sum - c
            
            if (nsum - nsumoffset)==0:  # match found
                if nxorsum==self.hints['xorsum']:
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
                    r = self._generate_tbuf_fromsum(nsum, noffset, c, nxorsum)
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
        
        

class V2(Solver.sumAndSplitPointAndBinaryDiff.V2):  
    def __init__(self):
        super(V2, self).__init__()
        self.hints['xorsum'] = 0x00
        
    
    def solve(self, callback=None):
        # temporary data buffer
        self.tbuf = bytearray([self.hints['interval'][1]]*self.hints['length'])
        self.callback = callback
        
        if self.hints['sum']==0:
            self._found_solution(tbuf)
        else:
            #self._generate_tbuf_fromsum(self.hints['sum'] - (self.hints['interval'][1]*self.hints['length']), 0, self.hints['interval'][0])
            self._generate_tbuf_fromsum(self.hints['sum'], 0, self.hints['interval'][0], 0)
        
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
        
        
        if cc<cmin:
            exit()

        cmin-= 1
        
        ret = 0
        while c > cmin:
            self.tbuf[offset] = c
            nsum = sum - c
            nxorsum = xorsum ^ c
            
            if noffset==(self.hints['length']-1):
                nxorsum = nxorsum ^ self.tbuf[offset+1]
                if (nsum - nsumoffset)==0:
                    if nxorsum==self.hints['xorsum']:
                        r = self._found_solution(self.tbuf, offset)
                        if r:
                            ret = r-1
                            break
                    else:
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
