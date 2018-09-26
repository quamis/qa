#include <iostream>
using namespace std;

#define BUFFER_SIZE 8

void print_tbuf(unsigned char tbuf[BUFFER_SIZE]) 
{
	unsigned char i;
	unsigned char altsum = 0;
    unsigned char rawsum = 0;
    unsigned char xorsum = 0;
	
	unsigned char xorsumshifted1 = 0;
	unsigned char xorsumshifted2 = 0;
	
	printf("    0x");
	for(i=0; i<BUFFER_SIZE; i++) {
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
	printf("        '");
	for(i=0; i<BUFFER_SIZE; i++) {
		printf("%c", tbuf[i]);
	}
	printf("'");
	
	printf("\n", altsum, rawsum, xorsum, xorsumshifted1, xorsumshifted2);
}


// run as 
//  $ g++ -O3  ./v1.cpp && time ./a.exe  | wc -l

int main() 
{
    unsigned char tbuf[BUFFER_SIZE];
	int c[BUFFER_SIZE];
	
	/* // 12345678
	unsigned char hint_rawsum=0xb8;
	unsigned char hint_altsum=0x58;
	unsigned char hint_xorsum=0x08;
	unsigned char hint_xorsumshifted1=0x1a;
	unsigned char hint_xorsumshifted2=0x12;
	unsigned char hint_interval_max=0x72;
	unsigned char hint_interval_min=0x20;
	*/
	
	/*
	// ane0
	unsigned char hint_rawsum=0x64;
	unsigned char hint_altsum=0x28;
	unsigned char hint_xorsum=0x5a;
	unsigned char hint_xorsumshifted1=0x4a;
	unsigned char hint_xorsumshifted2=0x15;
	unsigned char hint_interval_max=0x6e;
	unsigned char hint_interval_min=0x30;
	unsigned char hint_binarycomparison=0b0001;
	*/
	
	// 12343212
	unsigned char hint_rawsum=0x92;
	unsigned char hint_altsum=0x82;
	unsigned char hint_xorsum=0x06;
	unsigned char hint_xorsumshifted1=0x20;
	unsigned char hint_xorsumshifted2=0x22;
	unsigned char hint_interval_max=0x34;
	unsigned char hint_interval_min=0x31;
	unsigned char hint_binarycomparison=0b01000111;
	
	
	int altsum = 0;
    int rawsum = 0;
    int xorsum = 0;
	int xorsumshifted1 = 0;
	int xorsumshifted2 = 0;
		
	
	#define _start_loop(index, from, to) 												\
		for (c[index]=from; c[index]>=to; c[index]--) {									\
			tbuf[index] = c[index];														\
			rawsum+= c[index];															\
			altsum-= c[index];															\
			xorsum^= c[index];															\
			xorsumshifted1 = (xorsumshifted1<<1) ^ c[index];							\
			xorsumshifted2 = (xorsumshifted2>>1) ^ c[index];							\
	
	
	#define _close_loop(index) 									\
		xorsumshifted1 = (xorsumshifted1^c[index])>>1;			\
		xorsumshifted2 = (xorsumshifted2^c[index])<<1;			\
		xorsum^= c[index];										\
        altsum-= c[index];										\
        rawsum-= c[index];										\
    }
			
			
	// ((lxor2 << idx) & 0xff) ^ ch 
	
	_start_loop(0, hint_interval_max, hint_interval_min);
	_start_loop(1, hint_interval_max, hint_interval_min);
	_start_loop(2, hint_interval_max, hint_interval_min);
	_start_loop(3, hint_interval_max, hint_interval_min);
	_start_loop(4, hint_interval_max, hint_interval_min);
	_start_loop(5, hint_interval_max, hint_interval_min);
	_start_loop(6, hint_interval_max, hint_interval_min);
	_start_loop(7, hint_interval_max, hint_interval_min);


	bool has_max = false;
	bool has_min = false;
	for (int i=0; i<BUFFER_SIZE; i++) {
		if (tbuf[i]==hint_interval_max) {
			has_max = true;
		}
		if (tbuf[i]==hint_interval_min) {
			has_min = true;
		}
	}
		
	if (has_max && has_min && (xorsumshifted1 & 0xff)==hint_xorsumshifted1 && (rawsum & 0xff)==hint_rawsum) {
		print_tbuf(tbuf);
	}


	_close_loop(7);
	_close_loop(6);
	_close_loop(5);
	_close_loop(4);
	_close_loop(3);
	_close_loop(2);
	_close_loop(1);
	_close_loop(0);

    return 0;
}
