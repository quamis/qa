import sys, time, hashlib, zlib
import argparse
from termcolor import colored

parser = argparse.ArgumentParser(description='Solve(decompress)')
parser.add_argument('--str',     dest='str',	action='store', type=str,   default="",   help='TODO')
args = vars(parser.parse_args())


if __name__ == '__main__':
    print("Input string characteristics")
    bytes = args['str'].encode('utf-8')
    sbytes = sorted(bytearray(bytes), reverse=True)
    
    print("    as sorted str:    %s" % ( ' '.join( colored("%s" % (chr(c)), 'blue' if i%2==0 else 'red', 'on_white' if i%2==0 else 'on_yellow') for (i, c) in enumerate(sbytes))))
    print("    as sorted hex: 0x%s" % ( ''.join( colored("%02x" % (c), 'blue' if i%2==0 else 'red', 'on_white' if i%2==0 else 'on_yellow') for (i, c) in enumerate(sbytes))))
    
    
    print("    --length=%d" % (len(bytes)))
    
    print("    --sum=%d" % (sum(bytes)))
    print("        speed:10, ordering:False, len:4b")
    
    print("    --median=0x%02x (0x%02x->0x%02x)" % (sbytes[len(sbytes)//2], sbytes[0], sbytes[len(sbytes)-1]))
    print("        depends on sum, optimization hint, ordering:False, len:1b")
    
    lxor = 0x00
    for ch in bytes:
        lxor = lxor^ch
    print("    --xor=0x%02x" % (lxor))
    print("        speed:10, ordering:False, len:1b")
    
    print("\n    %s" % ("~" * 40))
    print("    --crc32=0x%06x" % (zlib.crc32(bytes) & 0xffffffff))
    print("        speed:9, ordering:True")
    
    h = hashlib.md5()
    h.update(bytes)
    print("    --md5=%s" % (h.hexdigest()))
    print("        speed:7, ordering:True, len=16b")
    
    h = hashlib.sha1()
    h.update(bytes)
    print("    --sha1=%s" % (h.hexdigest()))
    print("        speed:7, ordering:True")

    
    print("\n    %s" % ("~" * 40))
    print("    --interval=(0x%2x,0x%2x)" % (max(bytes), min(bytes)))
    print("        %d chars, len:2*char" % (max(bytes) - min(bytes)))
    
    dct = list(set(bytes))
    dct.sort(reverse=True)
    sd = ''.join("%s" % (chr(x)) for x in dct)
    print("    --dictionary='%s'" % (sd))
    print("        %d chars" % len(sd))
    #print("    --dictionary='%s'" % (''.join("0x%2x" % (x) for x in dct)))
    
    print("\n    %s" % ("~" * 40))