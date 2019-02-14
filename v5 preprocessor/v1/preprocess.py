import sys, zlib, hashlib, itertools

# @see https://gist.github.com/cincodenada/6557582
# @see https://www.falatic.com/index.php/108/python-and-bitwise-rotation
rotl = lambda val, r_bits: \
    (val << r_bits%8) & (2**8-1) | \
    ((val & (2**8-1)) >> (8-(r_bits%8)))
 
# Rotate right: 0b1001 --> 0b1100
rotr = lambda val, r_bits: \
    ((val & (2**8-1)) >> r_bits%8) | \
    (val << (8-(r_bits%8)) & (2**8-1))
 

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


def preprocess_none(data):
    return data
def unpreprocess_none(data):
    return data



def preprocess_001(data):
    for i in range(0, len(data)):
        data[i] = rotl(data[i], 1)
    return data

def unpreprocess_001(data):
    for i in range(0, len(data)):
        data[i] = rotr(data[i], 1)
    return data


def preprocess_002(data):
    d = data[0]
    for i in range(1, len(data)):
        data[i] = ((data[i] - d) + 256) % 256
    return data

def unpreprocess_002(data):
    # TODO
    return data

def preprocess_003(data):
    d = int(sum(data) / len(data))
    print(d)
    for i in range(1, len(data)):
        if (i%2==0):
            data[i] = (((d - data[i]) + 256) % 256)
        else:
            data[i] = (((d + data[i]) + 256) % 256)
    data.append(d)
    return data

def unpreprocess_003(data):
    # TODO
    return data

def preprocess_004(data):
    d = int(sum(data) / len(data))
    print(d)
    for i in range(1, len(data)):
        if (i%2==0):
            data[i] = rotr(data[i], i%8)
        else:
            data[i] = rotl(data[i], i%8)
    data.append(d)
    return data

def unpreprocess_004(data):
    # TODO
    return data

def preprocess_005(data):
    data2 = bytearray([])
    for i in range(0, len(data)):
        data2.append(data[i] & 0x0f)
        data2.append((data[i] & 0xf0) >> 4)
    return data2

def unpreprocess_005(data):
    data2 = bytearray([])
    for i in range(0, len(data), 2):
        data2.append(data[i] | (data[i+1] << 4))
    return data2

def preprocess_006(data):
    data1 = sorted(data)
    data2 = list([])
    d = data[0]
    for i in range(0, len(data), 2):
        data2.append((data[i] & 0x0f) | ((data[i+1] & 0x0f) << 4))
    return bytearray(data1 + data2)

def unpreprocess_006(data):
    data2 = bytearray([])
    dlen = int(2*len(data)/3)
    data_sorted = data[0:dlen]

    data_lmap = []
    for i in range(dlen, len(data)):
        data_lmap.append(data[i] & 0x0f)
        data_lmap.append((data[i] & 0xf0) >> 4)
    
    # aici ar trebui practic sa generez mai multe versiuni, si sa le validez cu un hash pana nimeresc versiunea buna...care (hash) momentan nu exista
    return data2



def preprocess_007(data):
    mc = hashlib.md5()
    mc.update(data)
    hash = mc.digest()
    #hash2 = mc.hexdigest()
    #print(hash2)

    for i in range(0, len(data)):
        data[i] = data[i] & 0b01111111

    for i in range(0, mc.digest_size):
        data.append(hash[i])
    
    return data

def unpreprocess_007(data):
    dlen = len(data) - 16 # 16 bytes for md5
    incompletedata = data[0:dlen]
    hash = ""
    for i in data[dlen:]:
        hash+= "%02x" % (i)

    return rec_call(incompletedata, hash)

def rec_call(data, targethash, currentindex=0):
    data[currentindex] = data[currentindex] & 0b01111111

    mc = hashlib.md5()
    mc.update(data)
    hash = mc.hexdigest()

    if hash==targethash:
        return data

    if (currentindex+1)<len(data):
        r = rec_call(data, targethash, currentindex+1)
        if not r is None:
            return r


    data[currentindex] = data[currentindex] | 0b10000000

    mc = hashlib.md5()
    mc.update(data)
    hash = mc.hexdigest()

    if hash==targethash:
        return data

    if (currentindex+1)<len(data):
        r = rec_call(data, targethash, currentindex+1)
        if not r is None:
            return r

def preprocess_008(data):
    data1 = bytearray([])
    data2 = bytearray([])
    for i in range(0, len(data)):
        data1.append((data[i] & 0b10000000) >> 7)
        data2.append(data[i] & 0b01111111)

    return bytearray(data1 + data2)

def unpreprocess_008(data):
    data1 = bytearray(data[0:len(data)//2])
    data2 = bytearray(data[len(data)//2:])
    data = bytearray([])
    for i in range(0, len(data1)):
        data.append((data1[i] << 7 )| data2[i])

    return data


def preprocess_009(data):
    data1 = bytearray([])
    data2 = bytearray([])
    data3 = bytearray([])
    data4 = bytearray([])
    data5 = bytearray([])
    data6 = bytearray([])
    data7 = bytearray([])
    data8 = bytearray([])
    for i in range(0, len(data)):
        data1.append((data[i] & 0b10000000) >> 7)
        data2.append((data[i] & 0b01000000) >> 6)
        data3.append((data[i] & 0b00100000) >> 5)
        data4.append((data[i] & 0b00010000) >> 4)
        data5.append((data[i] & 0b00001000) >> 3)
        data6.append((data[i] & 0b00000100) >> 2)
        data7.append((data[i] & 0b00000010) >> 1)
        data8.append((data[i] & 0b00000001) >> 0)

    return bytearray(data1 + data2 + data3 + data4 + data5 + data6 + data7 + data8)

def unpreprocess_009(data):
    data1 = bytearray(data[0*len(data)//8:1*len(data)//8])
    data2 = bytearray(data[1*len(data)//8:2*len(data)//8])
    data3 = bytearray(data[2*len(data)//8:3*len(data)//8])
    data4 = bytearray(data[3*len(data)//8:4*len(data)//8])
    data5 = bytearray(data[4*len(data)//8:5*len(data)//8])
    data6 = bytearray(data[5*len(data)//8:6*len(data)//8])
    data7 = bytearray(data[6*len(data)//8:7*len(data)//8])
    data8 = bytearray(data[7*len(data)//8:8*len(data)//8])
    data = bytearray([])
    for i in range(0, len(data1)):
        data.append((data1[i] << 7 ) | (data2[i] << 6 ) | (data3[i] << 5 ) | (data4[i] << 4 ) | (data5[i] << 3 ) | (data6[i] << 2 ) | (data7[i] << 1 ) | (data8[i] << 0 ))

    return data


def preprocess_010(data):
    b1 = 0
    b2 = 0
    b3 = 0
    b4 = 0
    b5 = 0
    b6 = 0
    b7 = 0
    b8 = 0
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
        d1.append(b)

        b = (data[i] & 0b01000000) >> 6
        b2+= b
        d2.append(b)

        b = (data[i] & 0b00100000) >> 5
        b3+= b
        d3.append(b)

        b = (data[i] & 0b00010000) >> 4
        b4+= b
        d4.append(b)

        b = (data[i] & 0b00001000) >> 3
        b5+= b
        d5.append(b)

        b = (data[i] & 0b00000100) >> 2
        b6+= b
        d6.append(b)

        b = (data[i] & 0b00000010) >> 1
        b7+= b
        d7.append(b)

        b = (data[i] & 0b00000001) >> 0
        b8+= b
        d8.append(b)

    print(len(data), b1, b2, b3, b4, b5, b6, b7, b8)
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

    print(d1)
    d1h = hashlib.md5(d1).digest()
    d2h = hashlib.md5(d2).digest()
    d3h = hashlib.md5(d3).digest()
    d4h = hashlib.md5(d4).digest()
    d5h = hashlib.md5(d5).digest()
    d6h = hashlib.md5(d6).digest()
    d7h = hashlib.md5(d7).digest()
    d8h = hashlib.md5(d8).digest()

    ndata.extend(d1h)
    ndata.extend(d2h)
    ndata.extend(d3h)
    ndata.extend(d4h)
    ndata.extend(d5h)
    ndata.extend(d6h)
    ndata.extend(d7h)
    ndata.extend(d8h)

    return ndata

def unpreprocess_010(data):
    dlen = int.from_bytes(data[0:2], byteorder='big')
    b1 = int.from_bytes(data[2:4], byteorder='big')
    b2 = int.from_bytes(data[4:6], byteorder='big')
    b3 = int.from_bytes(data[6:8], byteorder='big')
    b4 = int.from_bytes(data[8:10], byteorder='big')
    b5 = int.from_bytes(data[10:12], byteorder='big')
    b6 = int.from_bytes(data[12:14], byteorder='big')
    b7 = int.from_bytes(data[14:16], byteorder='big')
    b8 = int.from_bytes(data[16:18], byteorder='big')

    d1h = data[18+16*0:18+16*1]
    d2h = data[18+16*1:18+16*2]
    d3h = data[18+16*2:18+16*3]
    d4h = data[18+16*3:18+16*4]
    d5h = data[18+16*4:18+16*5]
    d6h = data[18+16*5:18+16*6]
    d7h = data[18+16*6:18+16*7]
    d8h = data[18+16*7:18+16*8]

    data1 = loop_call_010(bytearray([0] * dlen), {
        'dlen': dlen,
        'bits': b1,
        'hash': d1h,
    })
    data2 = loop_call_010(bytearray([0] * dlen), {
        'dlen': dlen,
        'bits': b2,
        'hash': d2h,
    })
    data3 = loop_call_010(bytearray([0] * dlen), {
        'dlen': dlen,
        'bits': b3,
        'hash': d3h,
    })
    data4 = loop_call_010(bytearray([0] * dlen), {
        'dlen': dlen,
        'bits': b4,
        'hash': d4h,
    })
    data5 = loop_call_010(bytearray([0] * dlen), {
        'dlen': dlen,
        'bits': b5,
        'hash': d5h,
    })
    data6 = loop_call_010(bytearray([0] * dlen), {
        'dlen': dlen,
        'bits': b6,
        'hash': d6h,
    })
    data7 = loop_call_010(bytearray([0] * dlen), {
        'dlen': dlen,
        'bits': b7,
        'hash': d7h,
    })
    data8 = loop_call_010(bytearray([0] * dlen), {
        'dlen': dlen,
        'bits': b8,
        'hash': d8h,
    })

    print(data1)
    print(data2)
    print(data3)
    print(data4)
    print(data5)
    print(data6)
    print(data7)
    print(data8)

    data = bytearray([])
    for i in range(0, dlen):
        data.append((data1[i] << 7 ) | (data2[i] << 6 ) | (data3[i] << 5 ) | (data4[i] << 4 ) | (data5[i] << 3 ) | (data6[i] << 2 ) | (data7[i] << 1 ) | (data8[i] << 0 ))

    return data

def iter_call_010(data, hints):
    # for some reason, itertool, just returns the same permutation...
    for i in range(0, hints['bits']):
        data[i] = 1

    print("")
    print("%s %d bits" % ("-"*20, hints['bits']))
    i = 0
    comb = itertools.permutations(data)
    for d in comb:
        i+=1
        print_010_data(d)
        hash = hashlib.md5(bytearray(d)).digest()
        if hash==hints['hash']:
            return d

def loop_call_010(data, hints):
    print("")
    print("%s %d bits" % ("-"*20, hints['bits']))
    for i in range(0, hints['bits']):
        data[i] = 1

    print_010_data(data)

    hash = hashlib.md5(data).digest()
    if hash==hints['hash']:
        return data

    return loop_call_010_rec(data, hints, 0, hints['bits'])
    

def loop_call_010_rec(data, hints, pluss, plusd):
    for s in range(hints['bits']-1, pluss, -1):
        if data[s]==1:
            data[s] = 0
            for d in range(plusd, hints['dlen']):
                if data[d]==0:
                    data[d] = 1
                    print_010_data(data)
                    hash = hashlib.md5(data).digest()
                    if hash==hints['hash']:
                        return data
                    
                    r = loop_call_010_rec(data, hints, s, d)
                    if not r is None:
                        return r

                    data[d] = 0
            data[s] = 1

def rec_call_010(data, hints, i=0):
    if i==0:
        print("")
        print("%s %d bits" % ("-"*20, hints['bits']))
        
    
    if hints['bits']>0:
        if (hints['dlen'] - i) < hints['bits']:
            return None

        data[i] = 1
        hints['bits'] -= 1
        if hints['bits']==0:
            print_010_data(data)
            hash = hashlib.md5(data).digest()
            if hash==hints['hash']:
                return data
            #return None

        if (i+1)<hints['dlen']:
            r = rec_call_010(data, hints, i+1)
            if not r is None:
                return r
        hints['bits'] += 1
        data[i] = 0

    data[i] = 0
    if hints['bits']==0:
        print_010_data(data)
        hash = hashlib.md5(data).digest()
        if hash==hints['hash']:
            return data
        return None

    if (i+1)<hints['dlen']:
        r = rec_call_010(data, hints, i+1)
        if not r is None:
            return r

def print_010_data(data):
    s = ""
    for i in range(0, len(data)):
        s+= ("%s" % ('.' if data[i]==0 else '*'))
    print("\r %s" % (s), end="", flush=False)

def preprocess_011(data):
    b1 = 0
    b2 = 0
    b3 = 0
    b4 = 0
    b5 = 0
    b6 = 0
    b7 = 0
    b8 = 0
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
        d1.append(b)

        b = (data[i] & 0b01000000) >> 6
        b2+= b
        d2.append(b)

        b = (data[i] & 0b00100000) >> 5
        b3+= b
        d3.append(b)

        b = (data[i] & 0b00010000) >> 4
        b4+= b
        d4.append(b)

        b = (data[i] & 0b00001000) >> 3
        b5+= b
        d5.append(b)

        b = (data[i] & 0b00000100) >> 2
        b6+= b
        d6.append(b)

        b = (data[i] & 0b00000010) >> 1
        b7+= b
        d7.append(b)

        b = (data[i] & 0b00000001) >> 0
        b8+= b
        d8.append(b)

    print(len(data), b1, b2, b3, b4, b5, b6, b7, b8)
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
    
    print_010_data(d1); print("");
    print_010_data(d2); print("");
    print_010_data(d3); print("");
    print_010_data(d4); print("");
    print_010_data(d5); print("");
    print_010_data(d6); print("");
    print_010_data(d7); print("");
    print_010_data(d8); print("");

    return ndata

def unpreprocess_011(data):
    dlen = int.from_bytes(data[0:2], byteorder='big')
    b1 = int.from_bytes(data[2:4], byteorder='big')
    b2 = int.from_bytes(data[4:6], byteorder='big')
    b3 = int.from_bytes(data[6:8], byteorder='big')
    b4 = int.from_bytes(data[8:10], byteorder='big')
    b5 = int.from_bytes(data[10:12], byteorder='big')
    b6 = int.from_bytes(data[12:14], byteorder='big')
    b7 = int.from_bytes(data[14:16], byteorder='big')
    b8 = int.from_bytes(data[16:18], byteorder='big')

    d1h = int.from_bytes(data[18+4*0:18+4*1], byteorder='big')
    d2h = int.from_bytes(data[18+4*1:18+4*2], byteorder='big')
    d3h = int.from_bytes(data[18+4*2:18+4*3], byteorder='big')
    d4h = int.from_bytes(data[18+4*3:18+4*4], byteorder='big')
    d5h = int.from_bytes(data[18+4*4:18+4*5], byteorder='big')
    d6h = int.from_bytes(data[18+4*5:18+4*6], byteorder='big')
    d7h = int.from_bytes(data[18+4*6:18+4*7], byteorder='big')
    d8h = int.from_bytes(data[18+4*7:18+4*8], byteorder='big')

    data1 = loop_call_011(bytearray([0] * dlen), {
        'dlen': dlen,
        'bits': b1,
        'hash': d1h,
    })
    data2 = loop_call_011(bytearray([0] * dlen), {
        'dlen': dlen,
        'bits': b2,
        'hash': d2h,
    })
    data3 = loop_call_011(bytearray([0] * dlen), {
        'dlen': dlen,
        'bits': b3,
        'hash': d3h,
    })
    data4 = loop_call_011(bytearray([0] * dlen), {
        'dlen': dlen,
        'bits': b4,
        'hash': d4h,
    })
    data5 = loop_call_011(bytearray([0] * dlen), {
        'dlen': dlen,
        'bits': b5,
        'hash': d5h,
    })
    data6 = loop_call_011(bytearray([0] * dlen), {
        'dlen': dlen,
        'bits': b6,
        'hash': d6h,
    })
    data7 = loop_call_011(bytearray([0] * dlen), {
        'dlen': dlen,
        'bits': b7,
        'hash': d7h,
    })
    data8 = loop_call_011(bytearray([0] * dlen), {
        'dlen': dlen,
        'bits': b8,
        'hash': d8h,
    })

    data = bytearray([])
    for i in range(0, dlen):
        data.append((data1[i] << 7 ) | (data2[i] << 6 ) | (data3[i] << 5 ) | (data4[i] << 4 ) | (data5[i] << 3 ) | (data6[i] << 2 ) | (data7[i] << 1 ) | (data8[i] << 0 ))

    return data

def loop_call_011(data, hints):
    print("")
    print("%s %d bits" % ("-"*20, hints['bits']))
    for i in range(0, hints['bits']):
        data[i] = 1

    print_010_data(data)

    hash = zlib.crc32(data)
    if hash==hints['hash']:
        return data

    return loop_call_011_rec(data, hints, 0, hints['bits'])
    

def loop_call_011_rec(data, hints, pluss, plusd):
    for s in range(hints['bits']-1, pluss, -1):
        if data[s]==1:
            data[s] = 0
            for d in range(plusd, hints['dlen']):
                if data[d]==0:
                    data[d] = 1
                    if s%3==0 and d%10==0:
                        print_010_data(data)
                    hash = zlib.crc32(data)
                    if hash==hints['hash']:
                        return data
                    
                    r = loop_call_011_rec(data, hints, s, d+1)
                    if not r is None:
                        return r

                    data[d] = 0
                    
                if data[d]==1:  # optimization
                    return None
            data[s] = 1
            
        if data[s]==0:  # optimization
            return None

def rec_call_011(data, hints, i=0):
    if i==0:
        print("")
        print("%s %d bits" % ("-"*20, hints['bits']))
        
    
    if hints['bits']>0:
        if (hints['dlen'] - i) < hints['bits']:
            return None

        data[i] = 1
        hints['bits'] -= 1
        if hints['bits']==0:
            print_010_data(data)
            hash = zlib.crc32(data)
            if hash==hints['hash']:
                return data
            #return None

        if (i+1)<hints['dlen']:
            r = rec_call_011(data, hints, i+1)
            if not r is None:
                return r
        hints['bits'] += 1
        data[i] = 0

    data[i] = 0
    if hints['bits']==0:
        print_010_data(data)
        hash = zlib.crc32(data)
        if hash==hints['hash']:
            return data
        return None

    if (i+1)<hints['dlen']:
        r = rec_call_011(data, hints, i+1)
        if not r is None:
            return r

def print_010_data(data):
    s = ""
    for i in range(0, len(data)):
        s+= ("%s" % ('.' if data[i]==0 else '*'))
    print("\r %s" % (s), end="", flush=False)


data = bytearray(open('img1.jpg', 'rb').read(32)) 

sys.setrecursionlimit(3000)

od = hashlib.sha256()
od.update(data)
print('Original data:     % 9d, %s'  % (len(data), od.hexdigest()))

#test_algo(data, preprocess_none, unpreprocess_none)
#test_algo(data, preprocess_010, unpreprocess_010)

test_algo_nocompress(data, preprocess_none, unpreprocess_none)
test_algo_nocompress(data, preprocess_011, unpreprocess_011)