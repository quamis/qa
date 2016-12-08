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

    #gbytes = {}
    #for ch in range(min(bytes), max(bytes)+1, 1):
    #    gbytes[ch] = 0
    #for ch in bytes:
    #    if not ch in gbytes:
    #        gbytes[ch] = 0
    #    gbytes[ch]+= 1
        
    ###########################################
    
    print("    as sorted str:    %s" % ( ' '.join( colored("%s" % (chr(c)), 'blue' if i%2==0 else 'red', 'on_white' if i%2==0 else 'on_yellow') for (i, c) in enumerate(sbytes))))
    print("    as sorted hex: 0x%s" % ( ''.join( colored("%02x" % (c), 'blue' if i%2==0 else 'red', 'on_white' if i%2==0 else 'on_yellow') for (i, c) in enumerate(sbytes))))
    
    
    print("    --length=%d" % (len(bytes)))
    
    print("    --sum=%d" % (sum(bytes)))
    print("        speed:10, ordering:False, len:4b")
    
    print("    --median=0x%02x (0x%02x->0x%02x)" % (sbytes[len(sbytes)//2], sbytes[0], sbytes[len(sbytes)-1]))
    print("        depends on sum, optimization hint, ordering:False, len:1b")
    

    differences = [i-j for i, j in zip(sbytes[:-1], sbytes[1:])]
    sdiff = sorted(list(set(differences)), reverse=True)
    spoints = []
    mid = len(sbytes)//2
    for (i, d) in enumerate(differences):
        score = 1.0*(float(mid - abs(mid - i))/mid) + 1.35*(float(d)/(1+max(sbytes) - min(sbytes)))
        spoints.append((score, d, i, sbytes[i]))
    
    #spoints = sorted(spoints, key=lambda sp: (((mid - abs(mid - sp[1]))/float(mid))*1000 + sp[0]*1000), reverse=True)
    #spoints = sorted(spoints, key=lambda sp: sp[0]*1000, reverse=True)
    
    #print("-" * 40)
    #for s in spoints:
    #    print("    > %c @%02d   diff:%d score:%.3f" % (s[3], s[2], s[1], s[0]))
        
    spoints = sorted(spoints, key=lambda sp: sp[0], reverse=True)
    
    #print("-" * 40)
    #for s in spoints:
    #    print("    > %c @%02d   diff:%d score:%.3f" % (s[3], s[2], s[1], s[0]))
    
    spoint = spoints[0]
    print("    --splitPoint=0x%02x,0x%02x (@%d, %c)" % (spoint[2], spoint[3], spoint[2], spoint[3], ))
    print("        depends on sum, optimization hint, ordering:False, len:2b")
    print("        like median, but not necessarily in the middle, but at a split point.")
    print("            Try with abcdefz, should return 'z@0'")
    print("            Try with aaabbbcccfgh, should return 'c@5'")
    print("            Try with abcdefghijklm, should return 'g@6'")
    
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