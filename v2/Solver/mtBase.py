# -*- coding: utf-8 -*-
import sys, time

import Solver.Base
import Solver.sum
import Solver.sumAndSplitPoint
import Solver.sumAndSplitPointAndBinaryDiff
import Solver.sumAndSplitPointAndBinaryDiffAndXorSum
from Solver.Base import CallbackResult

class SolverTracer(Solver.sumAndSplitPointAndBinaryDiffAndXorSum.V1):  
    def __init__(self):
        super(SolverTracer, self).__init__()
        
        self.settings = {}
        self.settings['warmup_time'] = 4
        self.settings['reportProgress_time'] = 2
        
        self.stats['solve::start'] = 0
        
        self.stats['_computeLimits::returns'] = []
        self.stats['_generate_tbuf_fromsum::calls'] = 0
        self.stats['_generate_tbuf_fromsum::reportingInterval'] = None
        
    def solve(self, callback=None):
        self.stats['solve::start'] = time.time()
        
        for i in range(self.hints['length']):
            self.stats['_computeLimits::returns'].append({
                'offset': i,
                'time': self.stats['solve::start'],
                'cmin': 0x00,
                'cmax': 0xff,
            })
        
        return super(SolverTracer, self).solve(callback)
        
    def _report_progress(self, tbuf, state):
        print("progress: %s, %s" % (state, self.print_buf_as_str(tbuf)))
        #return self.callbackProgress(tbuf, {})
        
    def _computeLimits(self, offset, cc):
        r = super(SolverTracer, self)._computeLimits(offset, cc)
        self.stats['_computeLimits::returns'][offset]['time'] = time.time()
        self.stats['_computeLimits::returns'][offset]['cmin'] = r[2]
        self.stats['_computeLimits::returns'][offset]['cmax'] = r[1]
        return r
        
    def print__computeLimits_returns(self, returns):
        ret = "\n"
        t = time.time()
        for r in returns:
            ret+= "    > %02d 0x%02x:0x%02x (%02d) (%s:%s), age: %.3fs\n" % (r['offset'], r['cmax'], r['cmin'], r['cmax'] - r['cmin'], chr(r['cmax']), chr(r['cmin']), t - r['time'])
        return ret
        
    def _generate_tbuf_fromsum(self, sum, offset, cc, xorsum):
        self.stats['_generate_tbuf_fromsum::calls']+= 1
        
        if self.stats['_generate_tbuf_fromsum::reportingInterval']:
            if self.stats['_generate_tbuf_fromsum::calls']>self.stats['_generate_tbuf_fromsum::reportingInterval']:
                self.stats['_generate_tbuf_fromsum::calls'] = 0
                self._report_progress(self.tbuf, "interval")
        elif self.stats['_generate_tbuf_fromsum::calls']%100 ==0 and time.time() - self.stats['solve::start']>self.settings['warmup_time']:
                self.stats['_generate_tbuf_fromsum::reportingInterval'] = (self.stats['_generate_tbuf_fromsum::calls']//self.settings['warmup_time'])*self.settings['reportProgress_time'];
                print(self.print__computeLimits_returns(self.stats['_computeLimits::returns']))
                print("%d seconds has passed, we looped %d times. Settings callback limits to %d ~= %d seconds" % (self.settings['warmup_time'], self.stats['_generate_tbuf_fromsum::calls'], self.stats['_generate_tbuf_fromsum::reportingInterval'], self.settings['reportProgress_time']))
        elif offset>(self.hints['length']-2):
            exit()
            self._report_progress(self.tbuf, "warmup")
            
        return super(SolverTracer, self)._generate_tbuf_fromsum(sum, offset, cc, xorsum)