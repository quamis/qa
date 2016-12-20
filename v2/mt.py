import multiprocessing
import time
import signal
import sys

def init_worker():
    signal.signal(signal.SIGINT, signal.SIG_IGN)

def worker():
    while(True):
        print("Working...")
        time.sleep(1.1234)
        

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