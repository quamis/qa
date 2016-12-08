# -*- coding: utf-8 -*-
import Solver.Base
import Solver.sum
from Solver.Base import CallbackResult

class Optimized(Solver.sum.RecursiveOptimized):
    def __init__(self):
        super(Optimized, self).__init__()
        self.callback = None
        self.hints['value'] = None
        self.hints['index'] = None
        
        self.indexMap = None
        
        self.stats['_computeLimits'] = {}
        self.stats['_computeLimits'][11] = 0
        self.stats['_computeLimits'][49] = 0
        self.stats['_computeLimits'][50] = 0
        self.stats['_computeLimits'][51] = 0
        self.stats['_computeLimits'][99] = 0
        
        
    def initialize(self):
        self.indexMap = bytearray([0]*self.hints['length'])
        
        """
        string: n m l k j i h g f e d c b a
        index, value : 7, g (this is a 0-based offset)
                  n  m  l  k  j  i  h  g  f  e  d  c  b  a
                 11 11 11 11 11 49 50 51 99 99 99 99 99 99
                                     |^|
        """
        
        for (offset, v) in enumerate(self.indexMap):
            if offset<(self.hints['index']-1):
                self.indexMap[offset] = 11
            elif offset==(self.hints['index']-1):
                self.indexMap[offset] = 49
            elif offset==(self.hints['index']+0):
                self.indexMap[offset] = 50
            elif offset==(self.hints['index']+1):
                self.indexMap[offset] = 51
            elif offset>(self.hints['index']+1):
                self.indexMap[offset] = 99
                
                
                
                
    def _computeLimits(self, sum, offset, cc):
        self.stats['_computeLimits'][self.indexMap[offset]]+=1
        
        if self.indexMap[offset]==11:
            return(
                None,
                min(self.hints['interval'][0], sum, cc), 
                self.hints['value']
            )
            
        elif self.indexMap[offset]==49:
            return(
                None,
                min(self.hints['interval'][0], sum, cc), 
                self.hints['value']
            )
            
        elif self.indexMap[offset]==50:
            return(
                None,
                self.hints['value'],
                self.hints['value']
            )
            
        elif self.indexMap[offset]==51:
            return(
                None,
                min(self.hints['value']-1, sum, cc),
                self.hints['interval'][1]
            )
            
        elif self.indexMap[offset]==99:
            return(
                None,
                min(self.hints['value']-1, sum, cc),
                self.hints['interval'][1]
            )
            
        #return super(Optimized, self)._computeLimits(sum, offset, cc)
