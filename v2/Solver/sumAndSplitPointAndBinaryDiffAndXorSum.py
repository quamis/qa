# -*- coding: utf-8 -*-
import sys

import Solver.Base
import Solver.sum
import Solver.sumAndSplitPoint
import Solver.sumAndSplitPointAndBinaryDiff
from Solver.Base import CallbackResult


"""
gives less false positives than the base class, but it might actually slow down the find in some cases, and accelerate it slightly in others. 
it generally slows down things a bit, but it pre-checks a cheap hash
    for test_16_15 it gives 420 solutions instead of 6123, so it gives a lot less false-positives
    
Detailed:
    $ py test.py Solver_sum_RecursiveOptimized_withInterval_withSplitPoint_withBinaryDiff_V2.test_16_15
    .
    ----------------------------------------------------------------------
    Ran 1 test in 5.500s

    OK
    MATCH FOUND
        zsrrrpnmieeaaa
    {'_generate_tbuf_fromsum::reports': 2000, '_found_solution': {'calls': 6123}, '_generate_tbuf_fromsum::maxReports': 2000, '_computeLimits': {'bdo==1, o>=i': 0, 'dro==i': 692208, 'dro==0': 1, 'bdo==0': 346446, 'o==i': 345739, 'dro==drl': 152180, 'bdo==1, o<i': 134596}}
    _computeLimits
        bdo==0         :  346446
        bdo==1, o<i    :  134596
        bdo==1, o>=i   :       0
        dro==0         :       1
        dro==drl       :  152180
        dro==i         :  692208
        o==i           :  345739
    _found_solution
        calls          :    6123

    
    
    $ py test.py Solver_sum_RecursiveOptimized_withInterval_withSplitPoint_withBinaryDiff_withXorSum_V1.test_16_15
    .
    ----------------------------------------------------------------------
    Ran 1 test in 5.600s

    OK
    0
    MATCH FOUND
        zsrrrpnmieeaaa
    {'_found_solution': {'calls': 420}, '_generate_tbuf_fromsum::maxReports': 2000, '_generate_tbuf_fromsum::reports': 2000, '_computeLimits': {'bdo==0': 346446, 'dro==0': 1, 'bdo==1, o<i': 134596, 'dro==i': 692208, 'dro==drl': 152180, 'o==i': 345739, 'bdo==1, o>=i': 0}}
    _computeLimits
        bdo==0         :  346446
        bdo==1, o<i    :  134596
        bdo==1, o>=i   :       0
        dro==0         :       1
        dro==drl       :  152180
        dro==i         :  692208
        o==i           :  345739
    _found_solution
        calls          :     420


"""
class V1(Solver.sumAndSplitPointAndBinaryDiff.V2):  
    def __init__(self):
        super(V1, self).__init__()
        self.hints['xorsum'] = 0x00
        
        self.stats['_generate_tbuf_fromsum::printIntervalMax'] = 100000
        self.stats['_generate_tbuf_fromsum::printInterval'] = self.stats['_generate_tbuf_fromsum::printIntervalMax']
        
    def _determineComplexityRaw(self):
        points = []
        self.initialize()
        sum = self.hints['sum']

        maxsize = 0
        for offset in range(0, self.hints['length']):
            (r, c, cmin) = self._computeLimits(offset, max(min(self.hints['interval'][0], sum), self.hints['interval'][1]))
            cpl = {
                'offset': offset,
                'interval': [c, cmin, ],
                'size': abs(c - cmin)+1,
            }
            
            maxsize = max(maxsize, cpl['size'])
            
            sum-= (c+cmin)//2
            points.append(cpl)
            
        return {
            'points':       points,
            'maxsize':      maxsize,
        }
        
    def determineParalelizationPoints(self):
        #points = [{'size':d['size'], 'offset':d['offset'], } for d in self._determineComplexityRaw()]
        cplRaw = self._determineComplexityRaw()
        points = cplRaw['points']
        maxsize = self.hints['interval'][0]-self.hints['interval'][1]
        for (k, p) in enumerate(points):
            score = []
            if p['size']>1:
                if p['size']>4: # 4 is the number of cores. should be dynamic though:)
                    score.append(1.0 * (float(p['size']-1)/cplRaw['maxsize']))
                else:
                    score.append(10.0 * (float(p['size']-1)/cplRaw['maxsize']))
                
                score.append(10.0 * (float((self.hints['length'] - p['offset']))/self.hints['length']))
                
            p['_score'] = sum(score)
            points[k] = p

        points = sorted(points, key=lambda p: p['_score'], reverse=True)
        return points
        
        
    def solve(self, callback=None):
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
