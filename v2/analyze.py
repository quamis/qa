import sys, time, hashlib, zlib
import argparse

parser = argparse.ArgumentParser(description='Solve(decompress)')
parser.add_argument('--str',     dest='str',	action='store', type=str,   default="",   help='TODO')
args = vars(parser.parse_args())


if __name__ == '__main__':
    print("Input string characteristics")
    bytes = args['str'].encode('utf-8')
    
    print("    --length=%d" % (len(bytes)))
    
    print("    --sum=%d" % (sum(bytes)))
    print("        speed:10, ordering:False")
    
    lxor = 0x00
    for ch in bytes:
        lxor = lxor^ch
    print("    --xor=0x%02x" % (lxor))
    print("        speed:10, ordering:False")
    
    print("\n    %s" % ("~" * 40))
    print("    --crc32=0x%06x" % (zlib.crc32(bytes) & 0xffffffff))
    print("        speed:9, ordering:True")
    
    h = hashlib.md5()
    h.update(bytes)
    print("    --md5=%s" % (h.hexdigest()))
    print("        speed:7, ordering:True")
    
    h = hashlib.sha1()
    h.update(bytes)
    print("    --sha1=%s" % (h.hexdigest()))
    print("        speed:7, ordering:True")

    
    print("\n    %s" % ("~" * 40))
    print("    --interval=(0x%2x,0x%2x)" % (max(bytes), min(bytes)))
    print("        %d chars" % (max(bytes) - min(bytes)))
    
    dct = list(set(bytes))
    dct.sort()
    sd = ''.join("%s" % (chr(x)) for x in dct)
    print("    --dictionary='%s'" % (sd))
    print("        %d chars" % len(sd))
    #print("    --dictionary='%s'" % (''.join("0x%2x" % (x) for x in dct)))
    
    print("\n    %s" % ("~" * 40))