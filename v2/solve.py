import sys, time
import argparse

import Solver.sum
import Solver.sumAndMD5

parser = argparse.ArgumentParser(description='Solve(decompress)')
parser.add_argument('--length',     dest='length',	action='store', type=int,   default=None,   help='TODO')
parser.add_argument('--sum',        dest='sum', action='store', type=int,   default=None,       help='TODO')
parser.add_argument('--md5',        dest='md5', action='store', type=str,   default=None,       help='TODO')
args = vars(parser.parse_args())

def hex2int(str):
    return int(str, 0)

"""
Optimization: 
    py to C/C++:http://stackoverflow.com/questions/3968499/how-to-embed-c-code-in-python-program

"""
    
    
if __name__ == '__main__':
    """
    >> "hashstring"
    py ./solve.py --length=10 --sum=1083 --md5=4b26ed207f470bbaeb44b62ff27d2d24
    
    >> "ab"
    time py ./solve.py --length=2 --sum=195 --md5=187ef4436122d1cc2f40dc2b92f0eba0
        V1
        0.132s
        {'_generate_tbuf_fromsum:found': 98, '_generate_tbuf_fromsum:misses:overflow': 9506, '_generate_tbuf_fromsum:calls': 9702}
    
    >> "abc"
    time py ./solve.py --length=3 --sum=294 --md5=900150983cd24fb0d6963f7d28e17f72
        V1
        0.97s
        {'_generate_tbuf_fromsum:found': 6951, '_generate_tbuf_fromsum:misses:overflow': 704721, '_generate_tbuf_fromsum:calls': 725845}
        
        V3:
        0.14s
        {'_generate_tbuf_fromsum:found': 252}
    
    >> "abac"
    time py ./solve.py --length=4 --sum=391 --md5=6624a35d3fedaacec13f7af3e51b491f
        V3:
        {'_generate_tbuf_fromsum:found': 404}
        real    0m0.110s

    >> "abus"
    time py ./solve.py --length=4 --sum=427 --md5=b14f39cf840010aae32008d9110189e4
    
    >> "abacu"
    time py ./solve.py --length=5 --sum=508 --md5=1f2e5b07d7609e233d15b225153a0a80
        
    
    >> "abacus"
    time py ./solve.py --length=6 --sum=623 --md5=13f27b1072bbf7719d0d267b083ff91c
        V3:
        !!! not found !!!
    
    
    >> "fedcba"
    time py ./solve.py --length=6 --sum=597 --md5=8df67bd6d5e123d52a9a966bb31cf719
    
    
    
    ~~~~~~~~~~~~~~~~~
    simple sum tests:
    time py ./solve.py --length=3 --sum=1
        1 results
    time py ./solve.py --length=3 --sum=2
        2 results
    time py ./solve.py --length=3 --sum=3
        3 results
    time py ./solve.py --length=3 --sum=4
        4 results
    time py ./solve.py --length=3 --sum=5
        5 results
    """
    #slv = Solver.sum.V3()
    slv = Solver.sumAndMD5.V1()
    
    slv.setHint('length', args['length'])
    slv.setHint('sum', args['sum'])
    slv.setHint('md5', args['md5'])
    
    def _evt_solved(buf):
        print(buf)
        
    slv.solve(callback=_evt_solved)
    
    #for t in slv.solve():
    #    print(t)
