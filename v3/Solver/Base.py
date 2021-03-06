# -*- coding: utf-8 -*-
import time
import collections, operator

class Base(object):
    def __init__(self):
        self.hints = {
            # the length of the output data
            'length':   None,       
            
            # the sum of the output data
            'sum':      None,
            
            # the md5 sum of the output data
            'md5': None,
        }
        
        self.stats = {}
        
    def setHint(self, hint, value):
        self.hints[hint] = value
        return self
        
    def _progress(self, data):
        # print progress
        pass

    def _solutionFound(self, output, data):
        # a possible solution was found. 
        # return True to stop iterating, and give up searching for solutions
        return False
        
    def solve(self):
        pass
    
    def initialize(self):
        pass    
    
    def print_obj(self, obj, key, depth=0):
        if key is None:
            rsort = sorted(obj.items(), key=(operator.itemgetter(0)))
        else:
            rsort = sorted(obj[key].items(), key=operator.itemgetter(0))
        
        ret = ""
        if not key is None:
            ret+=("\n%s%s" % ("    "*depth, key))
        for (k, v) in rsort:
            if isinstance(v, int):
                ret+=("\n%s    %-20s: %10d" % ("    "*depth, k, v))
            elif isinstance(v, dict):
                ret+=("\n%s    %-20s: %s" % ("    "*depth, k, self.print_obj(v, None, depth+1)))
        return ret
    
    def destroy(self):
        print(self.stats)
        
        if 'solve_lin' in self.stats:
            print(self.print_obj(self.stats, 'solve_lin'))
        
        if '_computeLimits' in self.stats:
            _computeLimits = sorted(self.stats['_computeLimits'].items(), key=operator.itemgetter(0))
            
            print("_computeLimits" % ())
            for (k, v) in _computeLimits:
                print("    %-15s: %7d" % (k, v))
                
        if '_found_solution' in self.stats:
            _found_solution = sorted(self.stats['_found_solution'].items(), key=operator.itemgetter(0))
            
            print("_found_solution" % ())
            for (k, v) in _found_solution:
                print("    %-15s: %7d" % (k, v))
        
    def print_tbuf(self, tbuf):
        s = "tbuf:"
        sum = 0
        altsum = 0;
        xor = 0;
        for i in range(0, len(tbuf)):
            s+= "%02x" % (tbuf[i])
            
            if i % 2==0:
                altsum+= tbuf[i]
            else:
                altsum-= tbuf[i]
                
            sum+=tbuf[i]
            
            xor^= tbuf[i]
        
        s+= "    (%02x, %02x, %02x)" % (sum, altsum, xor)
        return s
    
    def print_buf_as_sum(self, tbuf):
        sum = 0
        for i in range(0, len(tbuf)):
            sum+=tbuf[i]
        
        return sum
        
    def print_buf_as_str(self, tbuf):
        s = ""
        
        for i in range(0, len(tbuf)):
            s+= "%s" % (chr(tbuf[i]))

        return s
        
    def print_buf_as_binarydiff(self, tbuf):
        s = ""
        binarydiff = ""
        lch = tbuf[0]
        for ch in tbuf:
            binarydiff+= "%d" % (0 if lch==ch else 1)
            lch = ch
        
        return binarydiff
        
 

#class CallbackResult(object):
#   __slots__ = ('up', 'skipSibling')
#   def __init__(self):
#       self.up = None
#       self.skipSibling = None

CallbackResult = collections.namedtuple('CallbackResult', ['up', 'skipSibling', ])    
CallbackResult.__new__.__defaults__ = (0,) * len(CallbackResult._fields)

