import sys, zlib, hashlib

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


data = bytearray(open('img1.jpg', 'rb').read(2048)) 

sys.setrecursionlimit(3000)

od = hashlib.sha256()
od.update(data)
print('Original data:     % 9d, %s'  % (len(data), od.hexdigest()))

test_algo(data, preprocess_none, unpreprocess_none)

test_algo(data, preprocess_009, unpreprocess_009)