# -*- coding: utf-8 -*-
import Solver.Base
import Solver.sum
from Solver.Base import CallbackResult

class Optimized(Solver.sum.RecursiveOptimized_V2):
    def __init__(self):
        super(Optimized, self).__init__()
        self.callback = None
        self.hints['value'] = None
        self.hints['index'] = None
        
        self.indexMap = None
        
        self.stats['_computeLimits'] = {}
        self.stats['_computeLimits'][0x1] = 0
        self.stats['_computeLimits'][0x6] = 0
        self.stats['_computeLimits'][0x7] = 0
        self.stats['_computeLimits'][0x8] = 0
        self.stats['_computeLimits'][0x9] = 0
        self.stats['_computeLimits'][0xa] = 0
        self.stats['_computeLimits'][0xf] = 0
        
        
    def initialize(self):
        self.indexMap = bytearray([0]*self.hints['length'])
        
        """
        string: n m l k j i h g f e d c b a
        index, value : 7, g (this is a 0-based offset)
                nmlkjihgfedcba
                166666789aaaaf
                -.....|^|....-
        """
        
        for (offset, v) in enumerate(self.indexMap):
            if offset==0:
                self.indexMap[offset] = 0x1
            elif offset==(self.hints['length']-1):
                self.indexMap[offset] = 0xf
            elif offset<(self.hints['index']-1):
                self.indexMap[offset] = 0x6
            elif offset==(self.hints['index']-1):
                self.indexMap[offset] = 0x7
            elif offset==(self.hints['index']+0):
                self.indexMap[offset] = 0x8
            elif offset==(self.hints['index']+1):
                self.indexMap[offset] = 0x9
            elif offset>(self.hints['index']+1):
                self.indexMap[offset] = 0xa
            
                
                
    def _computeLimits(self, sum, offset, cc):
        self.stats['_computeLimits'][self.indexMap[offset]]+=1
        
        if    self.indexMap[offset]==0x1:
            return(
                None,
                self.hints['interval'][0],
                self.hints['interval'][0]
            )
        elif self.indexMap[offset]==0x6:
            return(
                None,
                min(self.hints['interval'][0], sum, cc), 
                self.hints['value']
            )
            
        elif self.indexMap[offset]==0x7:
            return(
                None,
                min(self.hints['interval'][0], sum, cc), 
                self.hints['value']
            )
            
        elif self.indexMap[offset]==0x8:
            return(
                None,
                self.hints['value'],
                self.hints['value']
            )
            
        elif self.indexMap[offset]==0x9:
            return(
                None,
                min(self.hints['value']-1, sum, cc),
                self.hints['interval'][1]
            )
            
        elif self.indexMap[offset]==0xa:
            return(
                None,
                min(self.hints['value']-1, sum, cc),
                self.hints['interval'][1]
            )
            
        elif self.indexMap[offset]==0xf:
            return(
                None,
                self.hints['interval'][1],
                self.hints['interval'][1]
            )
            
        #return super(Optimized, self)._computeLimits(sum, offset, cc)
