# -*- coding: utf-8 -*-
import time
import collections

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
    
    def destroy(self):
        print(self.stats)
        pass    
        
    def print_tbuf(self, tbuf):
        s = "tbuf:"
        sum = 0
        for i in range(0, len(tbuf)):
            s+= "%02x" % (tbuf[i])
            sum+=tbuf[i]
        
        s+= "    (%d)" % (sum)
        return s
        
        
    def print_buf_as_str(self, tbuf):
        s = "str:"
        
        sum = 0
        for i in range(0, len(tbuf)):
            s+= "%s" % (chr(tbuf[i]))
            sum+=tbuf[i]
        
        s+= "    (%d)" % (sum)
        return s
        
 

#class CallbackResult(object):
#   __slots__ = ('up', 'skipSibling')
#   def __init__(self):
#       self.up = None
#       self.skipSibling = None

CallbackResult = collections.namedtuple('CallbackResult', ['up', 'skipSibling', ])    
CallbackResult.__new__.__defaults__ = (0,) * len(CallbackResult._fields)

