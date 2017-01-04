#! /bin/python3
import time, sys, argparse

import Solver.mtBase

def worker():
    while(True):
        print("Working...")
        time.sleep(1.1234)
        
"""
if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    pool = multiprocessing.Pool(4, init_worker)
    try:
        for i in range(50):
            pool.apply_async(worker)

        #time.sleep(10)
        pool.close()
        pool.join()

    except KeyboardInterrupt:
        print("Caught KeyboardInterrupt, terminating workers")
        pool.terminate()
        pool.join()
"""

DBG = False
def countSolverHitsWithCallback(match, slv):
    def slv_callback(buf, params):
        if DBG:
            print("    %s" % slv.print_tbuf(buf))
        if match==buf:
            print("MATCH FOUND")
            print("    %s" % slv.print_buf_as_str(buf))
            global solutions
            solutions+=1
            
            # fast-return. as a final optimization
            #return (CallbackResult(len(buf)), None, None)
        
   
    if DBG:
        print("")
        print("-"*80)
        print("%s, %d, %d " % (type(slv), slv.hints['length'], slv.hints['sum']))
    
    global solutions
    solutions = 0
    
    
    manager = Solver.mtBase.SolverManager()
    manager.setSolver(slv)
    
    manager.initialize()
    manager.solve(callback=slv_callback)
    manager.destroy()
    
    if DBG:
        print("    solutions: %d" % (solutions))
        
    return solutions

def getSolver(len, sum, interval, index, value, xorsum, binarydiff):
    slv = Solver.mtBase.SolverTracer()
    # min width: ?
    
    slv.setHint('length', len)
    slv.setHint('sum', sum)
    slv.setHint('interval', (max(interval), min(interval)))
    slv.setHint('index', index)
    slv.setHint('value', value)
    slv.setHint('xorsum', xorsum)
    slv.setHint('binarydiff', binarydiff)
    
    return slv
    
if __name__ == "__main__":
    # def test_26_11_mt():
    slv = getSolver(26, 2479, (0x76,0x20), 0x15,0x4e, 0x39, (0,1,0,0,1,0,1,1,0,0,1,1,0,0,1,1,1,0,1,0,1,1,1,0,0,0,))
    countSolverHitsWithCallback('vtttssroooniiihfeeddaN    '.encode('utf-8'), slv)
    