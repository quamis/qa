import sys, zlib, hashlib, itertools

def crc32(data: bytes):
    return zlib.crc32(data)

def removeInstancesOfByte(data, byte):
    ndata = data.translate(None, byte.to_bytes(length=1, byteorder='big'))
    h = crc32(ndata)
    return [ndata, byte, len(data)-len(ndata), h]

def compress(data):
    return removeInstancesOfByte(data, 0x00)


def uncompress(ndata):
    data = ndata[0]
    byte = ndata[1]
    missingBytes = ndata[2]
    h = ndata[3]

    offsets = range(0, missingBytes)
    print(composeNewData(data, byte, offsets))


def composeNewData(data, byte, offsets):
    ndata = bytearray()
    lo = len(data)
    for o in reversed(offsets):
        ndata+= byte.to_bytes(length=1, byteorder='big') + data[lo-1:lo]

    return ndata
    # return removeInstancesOfByte(data, 0x00)


sys.setrecursionlimit(3000)

import unittest
class TestQa100_16b(unittest.TestCase):
    def setUp(self):
        self.datas = [
            bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, ]),
            bytearray([0x00, 0x00, 0x00, 0x03, 0x00, 0x00, 0x00, 0x00, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, ]),
            bytearray([0x01, 0x01, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, ]),
            bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, ]),
            bytearray([0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, ]),
            bytearray([0x00, 0x00, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x00, ]),
            bytearray([0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, ]),
            bytearray([0x00, 0x01, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, ]),
            bytearray([0x01, 0x00, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, ]),
            bytearray([0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, ]),

            bytearray([0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, 0x00, 0x01, ]),    # semi-worst-case?
        ]
        print("Running %s" % (self._testMethodName))


    def test_00(self):
        data = self.datas[0][:]
        print(compress(data))
        # self.assertEqual(compress(data), data)


    def test_01(self):
        data = self.datas[1][:]
        ndata = compress(data)
        print(ndata)
        print(uncompress(ndata))


if __name__ == '__main__':
    unittest.main()