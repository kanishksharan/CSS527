#ifndef SHA256_H_
#define SHA256_H_
#include <iostream>
#include <bitset>
#include <tuple>


#define BLOCK_SIZE_BITS 512

using namespace std;

typedef unsigned char byte;
class Sha256
{
private:
	//hash
	bitset<32> Hashes[8];
	

	//Apply block decomposition to message chunk to convert it to an array of 32 bit words
	void apply_block_decomposition(bitset<32>* const out, bitset<512> in);


	//helper function to get 32 bit range out a 512 bit set
	bitset<32> extract_32_bit(bitset<512>& in, int start_index);

	//apply small sigma zero function RotR(X, 7) + RotR(X, 18) + ShR(X, 3)
	bitset<32> small_sigma_zero(bitset<32> in);

	//apply small sigma one function RotR(X, 17) + RotR(X, 19) + ShR(X, 10)
	bitset<32> small_sigma_one(bitset<32> in);

	//apply big sigma zero function RotR(X, 2) + RotR(X, 13) + RotR(X, 22)
	bitset<32> big_sigma_zero(bitset<32> in);

	//apply big sigma one function RotR(X, 6) + RotR(X, 11) + RotR(X,25)
	bitset<32> big_sigma_one(bitset<32> in);

	//apply (X ^ Y ) + (!X ^ Z)
	bitset<32> ch(bitset<32> x, bitset<32> y, bitset<32> z);

	//apply (X ^ Y ) + (X ^ Z) + (Y ^ Z)
	bitset<32> maj(bitset<32> x, bitset<32> y, bitset<32> z);

	//circular right shift word by n bits
	bitset<32> rotr(bitset<32> input,unsigned int n);

	//concatenate all the 8 32-bit H values to 256-bit hash
	bitset<256> concat(bitset<32>* const Hs);

	

public:
	//constructor to initialize the H values
	Sha256();

	

	//Apply padding to incomplete last chunk of message with length less than or equal to n-(k+64 +1)
	//where n is block size and k is the smallest positive number of 0s and 64 is the length of the message 
	bitset<512> apply_last_chunk_padding(bitset<512> chunk, unsigned int chunk_size, unsigned long long message_size);


	//Generate padding for messages whose length is a multiple of 512
	bitset<512> apply_fresh_padding(unsigned long long message_size);

	//Apply padding to incomplete last chunk of message with length greater than or equal to n-(k+64+1)
	//and returns a pair of chunks  
	pair<bitset<512>, bitset<512>> apply_chunk_and_fresh_padding(bitset<512> chunk, unsigned int chunk_size, unsigned long long message_size);


	//Hashes a 512 bit input chunk
	void hash_chunk(bitset<512> chunk);

	//gets the current value of the H array as a 256-bit hash, (called at the end of an hashing session prior to reset Hs)
	bitset<256> get_current_hash();

	//gets the current value of the H array as a 256-bit hash, padded with 256 0 bits to make 512
	bitset<512> get_current_hash_512();

	//take the values of Hs back to a the original values in preparation for hashing a new message
	void reset_hashes();

};
#endif
