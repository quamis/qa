# -*- coding: utf-8 -*-
import sys

import Solver.Base

"""
slow, non-optimal
generates ALL combinations, not only in decreasing-sort-order
recursive
"""
class V1(Solver.Base.Base):
    def __init__(self):
        super(V1, self).__init__()
        self.stats['_generate_tbuf_fromsum:found'] = 0
        self.stats['_generate_tbuf_fromsum:calls'] = 0
        self.stats['_generate_tbuf_fromsum:misses:overflow'] = 0
    
    def solve(self):
        # temporary data buffer
        tbuf = bytearray([0]*self.hints['length'])
        
        for t in self._generate_tbuf_fromsum(tbuf[:], self.hints['sum'], 0, 0xff):
            #print(t)
            #print("\r%s\r" % self.stats)
            #if sum(t)==self.hints['sum']: # 
            #    yield t
            yield t
        #print("done")
        #print(self.stats)
    
    def _generate_tbuf_fromsum(self, tbuf, sum, offset, cc):
        self.stats['_generate_tbuf_fromsum:calls']+= 1
        if sum==0:
            self.stats['_generate_tbuf_fromsum:found']+= 1
            #self.print_tbuf(tbuf)
            yield tbuf
            
        if offset>=self.hints['length']:
            self.stats['_generate_tbuf_fromsum:misses:overflow']+= 1
            return
        
        for c in range(min(0xff, sum, cc), 0x00, -1):
            tbuf[offset] = c
            # propagate found solutions
            for t in self._generate_tbuf_fromsum(tbuf[:], sum-c, offset+1, c):
                yield t

class V1_1(Solver.Base.Base):
    def __init__(self):
        super(V1_1, self).__init__()
        self.stats['_generate_tbuf_fromsum:found'] = 0
        self.stats['_generate_tbuf_fromsum:calls'] = 0
        self.stats['_generate_tbuf_fromsum:misses:overflow'] = 0
    
    def solve(self):
        # temporary data buffer
        tbuf = bytearray([0]*self.hints['length'])
        
        for t in self._generate_tbuf_fromsum(tbuf, self.hints['sum'], 0, 0xff):
            #print(t)
            #print("\r%s\r" % self.stats)
            #if sum(t)==self.hints['sum']: # 
            #    yield t
            yield t
        #print("done")
        #print(self.stats)
    
    def _generate_tbuf_fromsum(self, tbuf, sum, offset, cc):
        self.stats['_generate_tbuf_fromsum:calls']+= 1
        if sum==0:
            self.stats['_generate_tbuf_fromsum:found']+= 1
            #self.print_tbuf(tbuf)
            yield tbuf
            
        if offset>=self.hints['length']:
            self.stats['_generate_tbuf_fromsum:misses:overflow']+= 1
            return
        
        for c in range(min(0xff, sum, cc), 0x00, -1):
            tbuf[offset] = c
            # propagate found solutions
            for t in self._generate_tbuf_fromsum(tbuf, sum-c, offset+1, c):
                yield t
        
        tbuf[offset] = 0
        
# not working
class V1_2(Solver.Base.Base):
    def __init__(self):
        super(V1_2, self).__init__()
        self.stats['_generate_tbuf_fromsum:found'] = 0
        self.stats['_generate_tbuf_fromsum:calls'] = 0
        self.stats['_generate_tbuf_fromsum:misses:overflow'] = 0
    
    def solve(self):
        # temporary data buffer
        tbuf = bytearray([0]*self.hints['length'])
        
        for t in self._generate_tbuf_fromsum(tbuf, self.hints['sum'], 0, 0xff):
            #print(t)
            #print("\r%s\r" % self.stats)
            #if sum(t)==self.hints['sum']: # 
            #    yield t
            self._found_solution(t)
        #print("done")
        #print(self.stats)
        
    def _found_solution(self, tbuf):
        yield tbuf
        
    def _generate_tbuf_fromsum(self, tbuf, sum, offset, cc):
        self.stats['_generate_tbuf_fromsum:calls']+= 1
        if sum==0:
            self.stats['_generate_tbuf_fromsum:found']+= 1
            #self.print_tbuf(tbuf)
            self._found_solution(tbuf)
            
        if offset>=self.hints['length']:
            self.stats['_generate_tbuf_fromsum:misses:overflow']+= 1
            return
        
        for c in range(min(0xff, sum, cc), 0x00, -1):
            tbuf[offset] = c
            # propagate found solutions
            for t in self._generate_tbuf_fromsum(tbuf, sum-c, offset+1, c):
                self._found_solution(t)
        
        tbuf[offset] = 0

class V1_3(Solver.Base.Base):  # TODO: convert this to a callback-hell-based solution:)
    def __init__(self):
        super(V1_3, self).__init__()
        self.callback = None
    
    def solve(self, callback=None):
        # temporary data buffer
        tbuf = bytearray([0x00]*self.hints['length'])
        self.callback = callback
        
        sys.stdout.write("\n\n")
        if self.hints['sum']==0:
            self._found_solution(tbuf)
        else:
            self._generate_tbuf_fromsum(tbuf, self.hints['sum'], 0, 0xff)
        
        self.callback = None
        
    def _found_solution(self, tbuf, depth):
        return self.callback(tbuf, depth)
        
    def _generate_tbuf_fromsum(self, tbuf, sum, offset, cc):
        if (self.hints['length']-offset)*0xff<sum:
            #print("f.ret: %s" % (self.print_tbuf(tbuf)))
            return 1+((sum - ((self.hints['length']-offset-1)*0xff))//0xff)
        
        tbuf[offset] = 0x00
        noffset = offset+1
        for c in range(min(0xff, sum, cc), 0x00, -1):
            tbuf[offset] = c
            nsum = sum-c
            if nsum==0:
                #print("match: %s" % (self.print_tbuf(tbuf)))
                r = self._found_solution(tbuf, offset)
                if r:
                    if r['return']:
                        return r['return']
            else:
                if noffset<self.hints['length']:
                    # check childs
                    r = self._generate_tbuf_fromsum(tbuf, nsum, noffset, c)
                    if r>0:
                        tbuf[offset] = 0x00
                        return r-1
                else:
                    tbuf[offset] = 0x00
                    return 0
        
        #print("retur: %s" % (self.print_tbuf(tbuf)))
        tbuf[offset] = 0x00
        return 0
        
        
"""
non functional
derived from V1, tried to use shortct-returns via yield's, but it still takes the same amount of time
recursive
"""
class V2(V1):
    #TODO: this should be a recursive call, and allow multiple-level returns (use exceptions?)
    def _generate_tbuf_fromsum(self, tbuf, sum, offset):
        self.stats['_generate_tbuf_fromsum:calls']+= 1
        if sum==0:
            self.stats['_generate_tbuf_fromsum:found']+= 1
            yield tbuf
            
        if offset>=self.hints['length']:
            self.stats['_generate_tbuf_fromsum:misses:overflow']+= 1
            return
        
        # max buffer value
        maxbv = min(0xff, sum)
        
        if sum>maxbv*(self.hints['length'] - offset):
            self.stats['_generate_tbuf_fromsum:misses:overflow']+= 1
            yield ("rewind", 3)
        
        for c in range(maxbv, 0x00, -1):
            tbuf[offset] = c
            # propagate found solutions
            for t in self._generate_tbuf_fromsum(tbuf, sum-c, offset+1):
                if t[0]=="rewind":
                    if t[1]>0:
                        yield ("rewind", t[1]-1)
                else:
                    yield t
                
                
"""
    seems accurate, fast, 0 false-positives
    non-recursive
"""
class V3(Solver.Base.Base):
    def __init__(self):
        super(V3, self).__init__()
        self.stats['_generate_tbuf_fromsum:found'] = 0
    
    def solve(self):
        # temporary data buffer
        tbuf = bytearray([0]*self.hints['length'])
        
        for t in self._generate_tbuf_fromsum(tbuf, self.hints['sum']):
            #print(t)
            #print("\r%s\r" % self.stats)
            yield t
        #print("done")
        #print(self.stats)
        
    def _generate_tbuf_fromsum(self, tbuf, sum):
        # step 1: generate the least-effort distribution
        tbuf = self._generate_tbuf_fromsum_step1(tbuf, sum)
        #self.print_tbuf(tbuf)
        self.stats['_generate_tbuf_fromsum:found']+= 1
        yield tbuf
        
        # step 2..n: walk the list from the right, and if possible add 1 unit to the right, and substract from the left, as long as the list is still sorted
        reloop = True
        lidxt=None
        while reloop:
            reloop = False
            
            idxf = None
            idxt = lidxt
            #for i in range(len(tbuf), 0, -1):
            i = len(tbuf)-1
            while i>=0:
                if not idxt is None and tbuf[idxt] - tbuf[i] < -1:
                    idxf = i
                    break
                    
                if idxt is None and tbuf[i] - tbuf[i-1] < 0:
                    idxt = i
                
                i-=1

            #print("%s, %s" % (idxf, idxt))
            if idxf is None or idxt is None:
                #raise StopIteration()
                return
            
            tbuf[idxf]-=1            
            tbuf[idxt]+=1
            
            if tbuf[idxt] - tbuf[idxf] < -1:
                lidxt = idxt
            else:
                lidxt = None
            
            reloop = True
            #self.print_tbuf(tbuf)
            self.stats['_generate_tbuf_fromsum:found']+= 1
            
            yield tbuf
            
        
    def _generate_tbuf_fromsum_step1(self, tbuf, sum):
        for i in range(0, len(tbuf)):
            v = min(0xff, sum)
            tbuf[i] = v
            sum-= v
        return tbuf
        
        
class V3_1(Solver.Base.Base):
    def __init__(self):
        super(V3_1, self).__init__()
        self.stats['_generate_tbuf_fromsum:found'] = 0
    
    def solve(self):
        # temporary data buffer
        tbuf = bytearray([0]*self.hints['length'])
        
        for t in self._generate_tbuf_fromsum(tbuf, self.hints['sum']):
            #print(t)
            #print("\r%s\r" % self.stats)
            yield t
        #print("done")
        #print(self.stats)
        
    def _generate_tbuf_fromsum(self, tbuf, sum):
        # step 1: generate the least-effort distribution
        tbuf = self._generate_tbuf_fromsum_step1(tbuf, sum)
        #self.print_tbuf(tbuf)
        self.stats['_generate_tbuf_fromsum:found']+= 1
        yield tbuf
        
        loops = 0
        
        # step 2..n: walk the list from the right, and if possible add 1 unit to the right, and substract from the left, as long as the list is still sorted
        reloop = True
        lidxt=None
        while reloop:
            reloop = False
            
            idxf = None
            #idxt = lidxt
            idxt = None
            
            i = len(tbuf)
            
            ops = []
            
            while i>0:
                i-=1
                
                print("  step %02d:%d" % (loops, i))
                loops+=1
                if loops>20:
                    return
                    
                # check if we should "distribuite" or "rollup"
                
                op = None
                
                # distribuite:1+
                pidv = 1 # prev index with different value
                while i-pidv>0 and tbuf[i]!=0 and tbuf[i]<tbuf[i-pidv]:
                    pidv+=1
                
                if op is None and tbuf[i]+1 <= tbuf[i-pidv]-1:
                    tbuf[i]+=1
                    tbuf[i-pidv]-=1
                    
                    reloop = True
                    op = "distrib:1"
                    
                    print("  > distrib:1+ from %s, move to %s, pidv: %s" % (i-pidv, i, pidv))
                    self.stats['_generate_tbuf_fromsum:found']+= 1
                    yield tbuf
                    break
                    
                    
                    
                
                    
                """
                if op is None and tbuf[i]+1 <= tbuf[i-1]-1:
                    tbuf[i]+=1
                    tbuf[i-1]-=1
                    
                    reloop = True
                    op = "distrib:1"
                    
                    print("  > distrib from %s, move to %s" % (i-1, i))
                    self.stats['_generate_tbuf_fromsum:found']+= 1
                    yield tbuf
                    break
                """
                """
                if op is None and tbuf[i]+1 == tbuf[i-1] and tbuf[i]+1 < tbuf[i-2]-1:
                    tbuf[i]+=1
                    tbuf[i-2]-=1
                    
                    reloop = True
                    op = "distrib:2"
                    
                    print("  > distrib from %s, move to %s" % (i-2, i))
                    self.stats['_generate_tbuf_fromsum:found']+= 1
                    yield tbuf
                    break
                """
                
                """
                # rollup
                if op is None and tbuf[i]<=tbuf[i-1] and tbuf[i]-1 < tbuf[i-1]+1 and tbuf[i]!=0 and tbuf[i-1]!=0:
                    tbuf[i]-=1
                    tbuf[i-1]+=1
                    
                    op = "rollup:1"
                    
                    print("  > rollup  from %s, move to %s, ---> %s" % (i, i-1, self.print_tbuf(tbuf)))
                """
                # rollup
                if op is None and not "rollup:1" in ops and tbuf[i]!=0 and tbuf[i-1]!=0 and tbuf[i]-1<=tbuf[i-1]+1 and tbuf[i-1]+1<=tbuf[i-2]:
                    tbuf[i]-=1
                    tbuf[i-1]+=1
                    
                    op = "rollup:1"
                    
                    print("  > rollup:1  from %s, move to %s, ---> %s" % (i, i-1, self.print_tbuf(tbuf)))
                    
                
                # distribuite:2
                pidv = 2 # prev index with different value
                #while i-pidv>0 and tbuf[i]!=0 and tbuf[i]<tbuf[i-pidv]:
                #    pidv+=1
                
                #if op is None and i+pidv<len(tbuf) and tbuf[i]!=0 and tbuf[i+pidv]==0 and tbuf[i]-1 >= tbuf[i+pidv]+1 and tbuf[i+pidv]+1 <= tbuf[i+pidv-1]:
                if op is None and i+pidv<len(tbuf) and tbuf[i]!=0 and tbuf[i+pidv]==0 and tbuf[i]-1 >= tbuf[i+pidv]+1:
                    tbuf[i]-=1
                    tbuf[i+pidv]+=1
                    
                    reloop = True
                    op = "distrib:2"
                    
                    print("  > distrib:2+ from %s, move to %s, pidv: %s" % (i, i+pidv, pidv))
                    self.stats['_generate_tbuf_fromsum:found']+= 1
                    yield tbuf
                    break
                
                ops.append(op)
                #print(ops)
                
                    
        
    def _generate_tbuf_fromsum_step1(self, tbuf, sum):
        for i in range(0, len(tbuf)):
            v = min(0xff, sum)
            tbuf[i] = v
            sum-= v
        return tbuf