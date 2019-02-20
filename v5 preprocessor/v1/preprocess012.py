import sys, zlib, hashlib, itertools

def compress(data):
    return bytearray(zlib.compress(data, 6))

def decompress(data):
    return bytearray(zlib.decompress(data))

def test_algo(data, preprocessfcn, unpreprocessfcn):
    print('%s %s' % ('-'*20, (preprocessfcn)))

    compressed_data = compress(preprocessfcn(data[:]))
    mc = hashlib.sha256()
    mc.update(compressed_data)
    print('Compressed data:   % 9d, %s' % (len(compressed_data), mc.hexdigest()))

    uncompressed_data = unpreprocessfcn(decompress(compressed_data))
    md = hashlib.sha256()
    md.update(uncompressed_data)
    print('Uncompressed data: % 9d, %s' % (len(uncompressed_data), md.hexdigest()))

    
def test_algo_nocompress(data, preprocessfcn, unpreprocessfcn):
    print('%s %s' % ('-'*20, (preprocessfcn)))

    compressed_data = preprocessfcn(data[:])
    mc = hashlib.sha256()
    mc.update(compressed_data)
    print('Compressed data:   % 9d, %s' % (len(compressed_data), mc.hexdigest()))

    uncompressed_data = unpreprocessfcn(compressed_data)
    md = hashlib.sha256()
    md.update(uncompressed_data)
    print('Uncompressed data: % 9d, %s' % (len(uncompressed_data), md.hexdigest()))


def print_bool_data(data):
    s = ""
    for i in range(0, len(data)):
        s+= ("%s" % ('.' if data[i]==0 else '*'))
    print("\r %s" % (s), end="", flush=False)

    
def preprocess_none(data):
    return data
def unpreprocess_none(data):
    return data

def preprocess_012(data):
    b1 = 0
    b2 = 0
    b3 = 0
    b4 = 0
    b5 = 0
    b6 = 0
    b7 = 0
    b8 = 0
    rs1 = 0
    rs2 = 0
    rs3 = 0
    rs4 = 0
    rs5 = 0
    rs6 = 0
    rs7 = 0
    rs8 = 0
    d1 = bytearray([])
    d2 = bytearray([])
    d3 = bytearray([])
    d4 = bytearray([])
    d5 = bytearray([])
    d6 = bytearray([])
    d7 = bytearray([])
    d8 = bytearray([])
    for i in range(0, len(data)):
        b = (data[i] & 0b10000000) >> 7
        b1+= b
        rs1+= (len(data) - i)*b
        d1.append(b)

        b = (data[i] & 0b01000000) >> 6
        b2+= b
        rs2+= (len(data) - i)*b
        d2.append(b)

        b = (data[i] & 0b00100000) >> 5
        b3+= b
        rs3+= (len(data) - i)*b
        d3.append(b)

        b = (data[i] & 0b00010000) >> 4
        b4+= b
        rs4+= (len(data) - i)*b
        d4.append(b)

        b = (data[i] & 0b00001000) >> 3
        b5+= b
        rs5+= (len(data) - i)*b
        d5.append(b)

        b = (data[i] & 0b00000100) >> 2
        b6+= b
        rs6+= (len(data) - i)*b
        d6.append(b)

        b = (data[i] & 0b00000010) >> 1
        b7+= b
        rs7+= (len(data) - i)*b
        d7.append(b)

        b = (data[i] & 0b00000001) >> 0
        b8+= b
        rs8+= (len(data) - i)*b
        d8.append(b)

    print("Input length: %d" % (len(data)))
    print("    bit sums: %d, %d, %d, %d, %d, %d, %d, %d" % (b1, b2, b3, b4, b5, b6, b7, b8))
    # print("    bit xor: 0x%02x, 0x%02x, 0x%02x, 0x%02x, 0x%02x, 0x%02x, 0x%02x, 0x%02x" % (bx1, bx2, bx3, bx4, bx5, bx6, bx7, bx8))
    print("    sums: 0x%04x, 0x%04x, 0x%04x, 0x%04x, 0x%04x, 0x%04x, 0x%04x, 0x%04x" % (rs1, rs2, rs3, rs4, rs5, rs6, rs7, rs8))
    ndata = bytearray([])
    ndata.extend(len(data).to_bytes(length=2, byteorder='big'))
    ndata.extend(b1.to_bytes(length=2, byteorder='big'))
    ndata.extend(b2.to_bytes(length=2, byteorder='big'))
    ndata.extend(b3.to_bytes(length=2, byteorder='big'))
    ndata.extend(b4.to_bytes(length=2, byteorder='big'))
    ndata.extend(b5.to_bytes(length=2, byteorder='big'))
    ndata.extend(b6.to_bytes(length=2, byteorder='big'))
    ndata.extend(b7.to_bytes(length=2, byteorder='big'))
    ndata.extend(b8.to_bytes(length=2, byteorder='big'))
    
    ndata.extend(rs1.to_bytes(length=2, byteorder='big'))
    ndata.extend(rs2.to_bytes(length=2, byteorder='big'))
    ndata.extend(rs3.to_bytes(length=2, byteorder='big'))
    ndata.extend(rs4.to_bytes(length=2, byteorder='big'))
    ndata.extend(rs5.to_bytes(length=2, byteorder='big'))
    ndata.extend(rs6.to_bytes(length=2, byteorder='big'))
    ndata.extend(rs7.to_bytes(length=2, byteorder='big'))
    ndata.extend(rs8.to_bytes(length=2, byteorder='big'))

    d1h = zlib.crc32(d1)
    d2h = zlib.crc32(d2)
    d3h = zlib.crc32(d3)
    d4h = zlib.crc32(d4)
    d5h = zlib.crc32(d5)
    d6h = zlib.crc32(d6)
    d7h = zlib.crc32(d7)
    d8h = zlib.crc32(d8)

    ndata.extend(d1h.to_bytes(length=4, byteorder='big'))
    ndata.extend(d2h.to_bytes(length=4, byteorder='big'))
    ndata.extend(d3h.to_bytes(length=4, byteorder='big'))
    ndata.extend(d4h.to_bytes(length=4, byteorder='big'))
    ndata.extend(d5h.to_bytes(length=4, byteorder='big'))
    ndata.extend(d6h.to_bytes(length=4, byteorder='big'))
    ndata.extend(d7h.to_bytes(length=4, byteorder='big'))
    ndata.extend(d8h.to_bytes(length=4, byteorder='big'))
    
    print_bool_data(d1); print("");
    print_bool_data(d2); print("");
    print_bool_data(d3); print("");
    print_bool_data(d4); print("");
    print_bool_data(d5); print("");
    print_bool_data(d6); print("");
    print_bool_data(d7); print("");
    print_bool_data(d8); print("");

    return ndata

def unpreprocess_012(data):
    dlen = int.from_bytes(data[0:2], byteorder='big')
    b1 = int.from_bytes(data[2:4], byteorder='big')
    b2 = int.from_bytes(data[4:6], byteorder='big')
    b3 = int.from_bytes(data[6:8], byteorder='big')
    b4 = int.from_bytes(data[8:10], byteorder='big')
    b5 = int.from_bytes(data[10:12], byteorder='big')
    b6 = int.from_bytes(data[12:14], byteorder='big')
    b7 = int.from_bytes(data[14:16], byteorder='big')
    b8 = int.from_bytes(data[16:18], byteorder='big')
    
    offset = 18
    size = 2
    rs1 = int.from_bytes(data[offset+size*0:offset+size*1], byteorder='big')
    rs2 = int.from_bytes(data[offset+size*1:offset+size*2], byteorder='big')
    rs3 = int.from_bytes(data[offset+size*2:offset+size*3], byteorder='big')
    rs4 = int.from_bytes(data[offset+size*3:offset+size*4], byteorder='big')
    rs5 = int.from_bytes(data[offset+size*4:offset+size*5], byteorder='big')
    rs6 = int.from_bytes(data[offset+size*5:offset+size*6], byteorder='big')
    rs7 = int.from_bytes(data[offset+size*6:offset+size*7], byteorder='big')
    rs8 = int.from_bytes(data[offset+size*7:offset+size*8], byteorder='big')

    offset = offset+size*8
    size = 4
    d1h = int.from_bytes(data[offset+size*0:offset+size*1], byteorder='big')
    d2h = int.from_bytes(data[offset+size*1:offset+size*2], byteorder='big')
    d3h = int.from_bytes(data[offset+size*2:offset+size*3], byteorder='big')
    d4h = int.from_bytes(data[offset+size*3:offset+size*4], byteorder='big')
    d5h = int.from_bytes(data[offset+size*4:offset+size*5], byteorder='big')
    d6h = int.from_bytes(data[offset+size*5:offset+size*6], byteorder='big')
    d7h = int.from_bytes(data[offset+size*6:offset+size*7], byteorder='big')
    d8h = int.from_bytes(data[offset+size*7:offset+size*8], byteorder='big')

    data1 = loop_call_012(bytearray([0] * dlen), {
        'dlen': dlen,
        'bits': b1,
        'rsum': rs1,
        'hash': d1h,
    })
    data2 = loop_call_012(bytearray([0] * dlen), {
        'dlen': dlen,
        'bits': b2,
        'rsum': rs2,
        'hash': d2h,
    })
    data3 = loop_call_012(bytearray([0] * dlen), {
        'dlen': dlen,
        'bits': b3,
        'rsum': rs3,
        'hash': d3h,
    })
    data4 = loop_call_012(bytearray([0] * dlen), {
        'dlen': dlen,
        'bits': b4,
        'rsum': rs4,
        'hash': d4h,
    })
    data5 = loop_call_012(bytearray([0] * dlen), {
        'dlen': dlen,
        'bits': b5,
        'rsum': rs5,
        'hash': d5h,
    })
    data6 = loop_call_012(bytearray([0] * dlen), {
        'dlen': dlen,
        'bits': b6,
        'rsum': rs6,
        'hash': d6h,
    })
    data7 = loop_call_012(bytearray([0] * dlen), {
        'dlen': dlen,
        'bits': b7,
        'rsum': rs7,
        'hash': d7h,
    })
    data8 = loop_call_012(bytearray([0] * dlen), {
        'dlen': dlen,
        'bits': b8,
        'rsum': rs8,
        'hash': d8h,
    })

    print("");
    
    data = bytearray([])
    for i in range(0, dlen):
        data.append((data1[i] << 7 ) | (data2[i] << 6 ) | (data3[i] << 5 ) | (data4[i] << 4 ) | (data5[i] << 3 ) | (data6[i] << 2 ) | (data7[i] << 1 ) | (data8[i] << 0 ))

    return data

def loop_call_012(data, hints):
    print("")
    print("%s %d bits" % ("-"*20, hints['bits']))
    for i in range(0, hints['bits']):
        data[i] = 1

    print_bool_data(data)
    print(" rsum: 0x%04x" %(hints['rsum']), end="")
    
    rsum = 0
    for i in range(0, hints['dlen']):
        rsum+= (hints['dlen']-i)*data[i] 
    
    

    hash = zlib.crc32(data)
    if hash==hints['hash']:
        return data

    return loop_call_012_rec(data, rsum, hints, 0, hints['bits'])
    

def loop_call_012_rec(data, rsum, hints, pluss, plusd):
    for s in range(hints['bits']-1, pluss-1, -1):
        if data[s]==1:
            if (rsum + s) < hints['rsum']:
                break
                

            data[s] = 0
            rsum-= (hints['dlen'] - s)
                
            for d in range(plusd, hints['dlen']):
                if data[d]==0:
                    if (rsum + d)<hints['rsum']:
                        break
                        
                    if (rsum + d)>(hints['rsum'] + hints['rsum']//2):   # not sure if this optimizes correctly, seems pretty random to use //2
                        break
                        
                    data[d] = 1
                    rsum+= (hints['dlen'] - d)
                    
                    if (s+d)%20==0:
                        print_bool_data(data)
                        print(" rsum: 0x%04x, 0x%04x" %(rsum, hints['rsum']), end="")

                    if rsum==hints['rsum'] or True:
                        #print_bool_data(data)
                        #return data
                        hash = zlib.crc32(data)
                        if hash==hints['hash']:
                            print_bool_data(data)
                            print(" rsum: 0x%04x, 0x%04x" %(rsum, hints['rsum']), end="")
                            return data
                    
                    r = loop_call_012_rec(data, rsum, hints, s-1, d+1)
                    if not r is None:
                        return r

                    data[d] = 0
                    rsum-= (hints['dlen'] - d)
                    
                if data[d]==1:  # optimization
                    return None
            data[s] = 1
            rsum+= (hints['dlen'] - s)
            
        if data[s]==0:  # optimization
            return None
            
            
#data = bytearray(open('img1.jpg', 'rb').read(96))
#                    1     2     3     4     5     6     7     8     9     0     1     2     3     4     5     6     7     8     9     0     1     2     3     4     5     6     7     8     9     0     1    2
#data = bytearray([0x01, 0x01, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, ])
#data = bytearray([0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x00, ])# semi-worst-case?
#data = bytearray([0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, ])
#data = bytearray([0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, ])    # semi-worst-case?
#data = bytearray([0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, ])
#data = bytearray([0x01, 0x00, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, ])
#data = bytearray([0x00, 0x01, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, ])
#data = bytearray([0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, ])
data = bytearray([0x00, 0x00, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x00, ])

sys.setrecursionlimit(3000)

od = hashlib.sha256()
od.update(data)
print('Original data:     % 9d, %s'  % (len(data), od.hexdigest()))

#test_algo(data, preprocess_none, unpreprocess_none)
#test_algo(data, preprocess_010, unpreprocess_010)

test_algo_nocompress(data, preprocess_none, unpreprocess_none)
test_algo_nocompress(data, preprocess_012, unpreprocess_012)