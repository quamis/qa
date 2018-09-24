#include <iostream>
using namespace std;

void print_tbuf(unsigned char tbuf[4]) 
{
	unsigned char i;
	unsigned char altsum = 0;
    unsigned char rawsum = 0;
    unsigned char xorsum = 0;
	
	unsigned char xorsumshifted1 = 0;
	unsigned char xorsumshifted2 = 0;
	
	printf("    0x");
	for(i=0; i<4; i++) {
		printf("%02x", tbuf[i]);
        rawsum+= tbuf[i];
		if (i %2==0) {
			altsum+= tbuf[i];
		}
		else {
			altsum-= tbuf[i];
		}
        xorsum^= tbuf[i];
		xorsumshifted1 = (xorsumshifted1<<1) ^ tbuf[i];
		xorsumshifted2 = (xorsumshifted2>>1) ^ tbuf[i];
	}
	
	printf("    (0x%02x, 0x%02x, 0x%02x, 0x%02x, 0x%02x)\n", altsum, rawsum, xorsum, xorsumshifted1, xorsumshifted2);
}


// run as 
//  $ g++ -O3  ./v1.cpp && time ./a.exe  | wc -l

int main() 
{
    unsigned char tbuf[4];
	unsigned char hint_altsum=0x00;
	unsigned char hint_xorsum=0x00;
	unsigned char hint_rawsum=0xc4;
	unsigned char hint_xorsumshifted1=0x1f;
	unsigned char hint_xorsumshifted2=0x23;
	
	int altsum = 0;
    int rawsum = 0;
    int xorsum = 0;
	int xorsumshifted1 = 0;
	int xorsumshifted2 = 0;
		
	int c0, c1, c2, c3;
	
	// ((lxor2 << idx) & 0xff) ^ ch 
	
    for (c0=0xff; c0>=0; c0--) {
        tbuf[0] = c0;
        rawsum+= c0;
        altsum+= c0;
        xorsum^= c0;
		xorsumshifted1 = (xorsumshifted1<<1) ^ c0;
		xorsumshifted2 = (xorsumshifted2>>1) ^ c0;
		
		for (c1=0xff; c1>=0; c1--) {
			tbuf[1] = c1;
			rawsum+= c1;
			altsum-= c1;
			xorsum^= c1;
			xorsumshifted1 = (xorsumshifted1<<1) ^ c1;
			xorsumshifted2 = (xorsumshifted2>>1) ^ c1;
			
			for (c2=0xff; c2>=0; c2--) {
				tbuf[2] = c2;
				rawsum+= c2;
				altsum+= c2;
				xorsum^= c2;
				xorsumshifted1 = (xorsumshifted1<<1) ^ c2;
				xorsumshifted2 = (xorsumshifted2>>1) ^ c2;
				
				for (c3=0xff; c3>=0; c3--) {
					tbuf[3] = c3;
					rawsum+= c3;
					altsum-= c3;
					xorsum^= c3;
					xorsumshifted1 = (xorsumshifted1<<1) ^ c3;
					xorsumshifted2 = (xorsumshifted2>>1) ^ c3;
					
					// 4983 results, 5.32s
					// if ((xorsumshifted1 & 0xff)==hint_xorsumshifted1 && rawsum==hint_rawsum) {
						
					// 65536 results, 5.5s
					// if ((xorsumshifted1 & 0xff)==hint_xorsumshifted1 && xorsum==hint_xorsum) {
						
					// 43690 results, 5.6s
					// if ((xorsumshifted1 & 0xff)==hint_xorsumshifted && altsum==hint_altsum) {
						
					// 65536 results, 5.5s
					// if ((xorsumshifted1 & 0xff)==hint_xorsumshifted1 && (xorsumshifted2 & 0xff)==hint_xorsumshifted2) {
						
						
					if ((xorsumshifted1 & 0xff)==hint_xorsumshifted1 && rawsum==hint_rawsum) {
						print_tbuf(tbuf);
					}
					
					xorsumshifted1 = (xorsumshifted1^c3)>>1;
					xorsumshifted2 = (xorsumshifted2^c3)<<1;
					xorsum^= c3;
					altsum+= c3;
					rawsum-= c3;
				}
				
				xorsumshifted1 = (xorsumshifted1^c2)>>1;
				xorsumshifted2 = (xorsumshifted2^c2)<<1;
				xorsum^= c2;
				altsum-= c2;
				rawsum-= c2;
			}
			
			xorsumshifted1 = (xorsumshifted1^c1)>>1;
			xorsumshifted2 = (xorsumshifted2^c1)<<1;
			xorsum^= c1;
			altsum+= c1;
			rawsum-= c1;
		}
		
		xorsumshifted1 = (xorsumshifted1^c0)>>1;
		xorsumshifted2 = (xorsumshifted2^c0)<<1;
		xorsum^= c0;
        altsum-= c0;
        rawsum-= c0;
    }

    return 0;
}
