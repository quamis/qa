# qa
v1+v2


depends on 
	-
	
next optimizations:
	x use xorsum to reduce the number of false-positives
	- use threads/processes (Pool) - limited to the number of CPU cores, and a process-manager would be needed
	- use C/C++/PyPy+CFFI
	- use OpenCL - it doesn't support recursive functions, so a non-resursive algorithm would have to be implemented
	
	
@see https://en.wikipedia.org/wiki/List_of_hash_functions

reverse a crc32 https://www.cosc.canterbury.ac.nz/greg.ewing/essays/CRC-Reverse-Engineering.html


You can model CRC-32 as a state machine
------

We will represent CRC-32 as a matrix product—this will allow us not only to compute the checksum of the kernel quickly, but also to reuse computation across files. The technique described in this section is a slight extension of the crc32_combine function in zlib, which Mark Adler explains here.

You can model CRC-32 as a state machine that updates a 32-bit state register for each incoming bit. The basic update operations for a 0 bit and a 1 bit are:
```
uint32 crc32_update_0(uint32 state) {
    // Shift out the least significant bit.
    bit b = state & 1;
    state = state >> 1;
    // If the shifted-out bit was 1, XOR with the CRC-32 constant.
    if (b == 1)
        state = state ^ 0xedb88320;
    return state;
}

uint32 crc32_update_1(uint32 state) {
    // Do as for a 0 bit, then XOR with the CRC-32 constant.
    return crc32_update_0(state) ^ 0xedb88320;
}
```

If you think of the state register as a 32-element binary vector, and use XOR for addition and AND for multiplication, then crc32_update_0 is a linear transformation; i.e., it can be represented as multiplication by a 32×32 binary transformation matrix. To see why, observe that multiplying a matrix by a vector is just summing the columns of the matrix, after multiplying each column by the corresponding element of the vector. The shift operation state >> 1 is just taking each bit i of the state vector and multiplying it by a vector that is 0 everywhere except at bit i − 1 (numbering the bits from right to left). The conditional final XOR state ^ 0xedb88320 that only happens when bit b is 1 can instead be represented as first multiplying b by 0xedb88320 and then XORing it into the state. 

@see https://www.bamsoftware.com/hacks/zipbomb/


optimize rust
-------

 - https://www.google.com/url?q=https%3A%2F%2Fwww.cberner.com%2F2019%2F03%2F30%2Fraptorq-rfc6330-rust-optimization%2F&sa=D&usd=2&usg=AFQjCNEn41IgzXIkyIAkbJM2PCEMMrtGVg
