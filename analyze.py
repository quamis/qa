import sys, time, hashlib, zlib, os, string, re, math
import argparse
from termcolor import colored

parser = argparse.ArgumentParser(description='Solve(decompress)')
parser.add_argument('--str',     dest='str',	action='store', type=str,   default=None,   help='TODO')
parser.add_argument('--file',    dest='file',	action='store', type=str,   default=None,   help='TODO')
parser.add_argument('-v',        dest='verbose', action='store', type=int,   default=0,   help='TODO')
args = vars(parser.parse_args())

def print_char(ch):
    #if chr(ch) in string.ascii_letters or chr(ch) in string.digits:
    if re.match(r"[a-zA-Z0-9\ \!\@\#\$\%\^\&\*\(\)\_\+\-\=\~\`\[\]\{\}\;\'\:\"\,\.\<\>\/\?]", chr(ch)) is None:
        return ("?")
    else:
        return ("%c" % (ch))
        
        

if __name__ == '__main__':
    print("Input string characteristics")
    bytes = None
    if args['str']:
        bytes = args['str'].encode('ascii')
        
    if args['file']:
        print("'%s'" % (args['file']))
        print("    os.path.isfile:%s" % (os.path.isfile(args['file'])))
        if os.path.isfile(args['file']):
            f = open(args['file'], 'rb')
            bytes = f.read()
            f.close()
    
    if bytes is None:
        print("No input specified")
        exit(1)
    
    sbytes = sorted(bytearray(bytes), reverse=True)

    gbytes = {}
    for ch in range(min(bytes), max(bytes)+1, 1):
        gbytes[ch] = 0
    for ch in bytes:
        gbytes[ch]+= 1
        
    ###########################################
    
    if args['verbose']>0:
        print("    as sorted str:    %s" % ( ' '.join( colored("%s" % (print_char(c)), 'blue' if i%2==0 else 'red', 'on_white' if i%2==0 else 'on_yellow') for (i, c) in enumerate(sbytes))))
        print("    as sorted hex: 0x%s" % ( ''.join( colored("%02x" % (c), 'blue' if i%2==0 else 'red', 'on_white' if i%2==0 else 'on_yellow') for (i, c) in enumerate(sbytes))))
        print("       sorted str:   '%s'" % ( ''.join( colored("%s" % (print_char(c)), 'white') for (i, c) in enumerate(sbytes))))
    
    
    print("    --length=%d" % (len(bytes)))
    
    print("    --sum=0x%08x (%d)" % (sum(bytes), sum(bytes)))
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
    
    if args['verbose']>2:
        print("-" * 40)
        for s in spoints:
            print("    > %s (0x%02x) @%02d   diff:%d score:%.3f" % (print_char(s[3]), s[3], s[2], s[1], s[0]))
        
    spoints = sorted(spoints, key=lambda sp: sp[0], reverse=True)
    
    #print("-" * 40)
    #for s in spoints:
    #    print("    > %s @%02d   diff:%d score:%.3f" % (print_char(s[3]), s[2], s[1], s[0]))
    
    spoffset = 0
    if spoints[spoffset][2]==0: # avoid interval limits
        spoffset+=1
    if spoints[spoffset][2]==len(sbytes)-1: # avoid interval limits
        spoffset+=1

    spoint = spoints[spoffset]
    print("    --splitPoint=0x%02x,0x%02x (@%d, %s)" % (spoint[2], spoint[3], spoint[2], print_char(spoint[3]), ))
    spoffset+=1
    spoint = spoints[spoffset]
    print("    --splitPoint(next pick)=0x%02x,0x%02x (@%d, %s)" % (spoint[2], spoint[3], spoint[2], print_char(spoint[3]), ))
    spoffset+=1
    spoint = spoints[spoffset]
    print("    --splitPoint(next pick)=0x%02x,0x%02x (@%d, %s)" % (spoint[2], spoint[3], spoint[2], print_char(spoint[3]), ))
    
    print("        depends on sum, optimization hint, ordering:False, len:2b")
    print("        like median, but not necessarily in the middle, but at a split point.")
    if args['verbose']>8:
        print("            Try with abcdefz, should return 'z@0'")
        print("            Try with aaabbbcccfgh, should return 'c@5'")
        print("            Try with abcdefghijklm, should return 'g@6'")
    
    lxor = 0x00
    for ch in bytes:
        lxor = lxor ^ ch
    print("    --xorsum=0x%02x" % (lxor))
    print("        speed:10, ordering:False, len:1b")
    
    lxor = 0x00
    idx=0
    for ch in bytes:
        lxor = ((lxor << 1) & 0xff) ^ ch 
        idx+=1
        
    print("    --xorsum shifted 1=0x%02x" % (lxor))
    print("        speed:10, ordering:False, len:1b")
    
    lxor = 0x00
    idx=0
    for ch in bytes:
        lxor = ((lxor >> 1) & 0xff) ^ ch 
        idx+=1
        
    print("    --xorsum shifted 2=0x%02x" % (lxor))
    print("        speed:10, ordering:False, len:1b")
    
    binarydiff = []
    lch = sbytes[0]
    for ch in sbytes:
        binarydiff.append(0 if lch==ch else 1)
        lch = ch
    print("    --binarydiff=%s" % ((''.join("%d" % (x) for x in binarydiff))))
    print("        (%s)" % (''.join("%s," % (x) for x in binarydiff)))
    print("        %dbits ~ %db" % (len(binarydiff), int(math.ceil(float(len(binarydiff))/8))))
    
    if args['verbose']>1:
        binaryDiffRSums = []
        binaryDiffRSumsV2 = []
        for (offset, v) in enumerate(binarydiff):
            binaryDiffRSums.append(sum(binarydiff[offset:]))
            binaryDiffRSumsV2.append(sum(binarydiff[offset+1:]))
            
        print("        binaryDiffRSums=   hex:'%s'" % ( ''.join( colored("%01x" % (bd), 'blue' if i%2==0 else 'red', 'on_white' if i%2==0 else 'on_yellow') for (i, bd) in enumerate(binaryDiffRSums))))
        print("        binaryDiffRSumsV2= hex:'%s'" % ( ''.join( colored("%01x" % (bd), 'blue' if i%2==0 else 'red', 'on_white' if i%2==0 else 'on_yellow') for (i, bd) in enumerate(binaryDiffRSumsV2))))
    
    
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

    dct = list(set(bytes))
    dct.sort(reverse=True)
    sd = ''.join("%s" % (print_char(x)) for x in dct)
    if len(sd)<16 or args['verbose']>2:
        print("    --dictionary='%s'" % (sd))
        print("        %db" % len(sd))
    #print("    --dictionary='%s'" % (''.join("0x%2x" % (x) for x in dct)))
    
    print("\n    %s" % ("~" * 40))
    print("    --interval=(0x%02x,0x%02x)" % (max(bytes), min(bytes)))
    print("        len:2b" % ())

    intervalIslands = []
    pch = min(sbytes)-1
    for ch in gbytes:
        if (ch-1) in gbytes and gbytes[ch-1]!=0 and gbytes[ch]==0:
            intervalIslands.append((pch+1, ch-1))
            pch=ch
        elif gbytes[ch]==0:
            pch=ch
    intervalIslands.append((pch+1, max(sbytes)))
    print("    --intervalIslands=%s" % (intervalIslands))
    print("        %d chars, len:2b" % (max(bytes) - min(bytes)))
    
    if args['verbose']>8:
        print("    --charCountDistribution:")
        for ch in range(0x00, 0xff+1, 1):
            print("        > %s (0x%02x) % 9d" % (print_char(ch), ch, gbytes[ch] if ch in gbytes else 0))
    
    print("\n    %s" % ("~" * 40))
