#include <fstream>
#include "sha256.h"


bitset<32> k_primes[] = {
	0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
	0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
	0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
	0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
	0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
	0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
	0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
	0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
};



bitset<32> operator +(bitset<32> a, bitset<32> b)
{
	unsigned long aInt = a.to_ulong();
	unsigned long bInt = b.to_ulong();
	return bitset<32>((aInt + bInt) % 0x100000000);
}



Sha256::Sha256()
{
	reset_hashes();
}


bitset<512> Sha256::apply_last_chunk_padding(bitset<512> chunk, unsigned int chunk_size, unsigned long long message_size)
{
	unsigned int missingBits = BLOCK_SIZE_BITS - chunk_size;
	
	chunk <<= missingBits;
	
	chunk[missingBits - 1] = true;
	
	chunk |= message_size;
	return chunk;

}

bitset<512> Sha256::apply_fresh_padding(unsigned long long message_size)
{
	bitset<512> output(0);
	
	output[511] = true;
	
	output |= message_size;
	return output;
}

pair<bitset<512>, bitset<512>> Sha256::apply_chunk_and_fresh_padding(bitset<512> chunk, unsigned int chunk_size, unsigned long long message_size)
{
	unsigned int missingBits = BLOCK_SIZE_BITS - chunk_size;
	
	chunk <<= missingBits;
	
	chunk[missingBits - 1] = true;
	bitset<512> fresh_chunk(0);
	
	fresh_chunk |= message_size;
	return pair<bitset<512>,bitset<512>>(chunk,fresh_chunk);
}

bitset<32> Sha256::extract_32_bit(bitset<512>& in, int start_index)
{
	bitset<32> output(0);
	for (size_t i = 0; i < 32; i++)
	{
		output <<= 1;
		
		if (in.test(511 - (i + start_index)))
		{
			
			output |= 1;

		}

	}

	return output;
}

void Sha256::apply_block_decomposition(bitset<32>* const out, bitset<512> in)
{
	
	for (int i = 0; i < 16; i++)
	{
		out[i] = extract_32_bit(in,i * 32);
		
	}
	
	for (int i = 16; i < 64; i++)
	{
		out[i] = small_sigma_one(out[i - 2])+ out[i - 7] + small_sigma_zero(out[i - 15]) + out[i - 16];
		
	}
}





bitset<32> Sha256::small_sigma_zero(bitset<32> in)
{
	
	return rotr(in, 7)^ rotr(in, 18)^(in >> 3);
	
}

bitset<32> Sha256::small_sigma_one(bitset<32> in)
{
	
	return rotr(in, 17) ^ rotr(in, 19)^(in >> 10);
	
}


bitset<32> Sha256::big_sigma_zero(bitset<32> in)
{
	
	return rotr(in, 2)^ rotr(in, 13)^rotr(in, 22);
	
}

bitset<32> Sha256::big_sigma_one(bitset<32> in)
{
	
	return rotr(in, 6)^ rotr(in, 11)^ rotr(in, 25);
	
}

bitset<32> Sha256::rotr(bitset<32> in, unsigned int n)
{
	
	
	unsigned int mask = (2 << (n - 1)) - 1;
	bitset<32> output(0);
	
	output |= (in.to_ulong() & mask);
	
	
	output <<= (32 - n);
	

	mask = (0xFFFFFFFF << n);
	
	output |= ((in.to_ulong() & mask)>>n);
	
	return output;	
}

bitset<32> Sha256::ch(bitset<32> x, bitset<32> y, bitset<32> z)
{
	
	bitset<32> temp = x;
	return (temp&y) ^ (x.flip() & z);
}

bitset<32> Sha256::maj(bitset<32> x, bitset<32> y, bitset<32> z)
{
	
	return (x&y) ^ (x&z) ^ (y&z);
}



bitset<256> Sha256::concat(bitset<32>* const Hs)
{
	bitset<256> output(0);
	for (int i = 0; i < 8; i++)
	{
		output <<= 32;
		output |= Hashes[i].to_ulong();
		

	}
	return output;
}

void Sha256::hash_chunk(bitset<512> chunk)
{
	
	bitset<32> words[64];
	apply_block_decomposition(words, chunk);

	
	bitset<32> a = Hashes[0];
	bitset<32> b = Hashes[1];
	bitset<32> c = Hashes[2];
	bitset<32> d = Hashes[3];
	bitset<32> e = Hashes[4];
	bitset<32> f = Hashes[5];
	bitset<32> g = Hashes[6];
	bitset<32> h = Hashes[7];
	for (int i = 0; i < 64; i++)
	{
		bitset<32> T1 = h + big_sigma_one(e) + ch(e, f, g) + k_primes[i] + words[i];
		bitset<32> T2 = big_sigma_zero(a) + maj(a, b, c);
		h = g;
		g = f;
		f = e;
		e = d + T1;
		d = c;
		c = b;
		b = a;
		a = T1 + T2;
		
		
	}
	Hashes[0] = Hashes[0] + a;
	Hashes[1] = Hashes[1] + b;
	Hashes[2] = Hashes[2] + c;
	Hashes[3] = Hashes[3] + d;
	Hashes[4] = Hashes[4] + e;
	Hashes[5] = Hashes[5] + f;
	Hashes[6] = Hashes[6] + g;
	Hashes[7] = Hashes[7] + h;
	
}




bitset<256> Sha256::get_current_hash()
{
	
	return concat(Hashes);
}


bitset<512> Sha256::get_current_hash_512()
{
	bitset<512> output(0);
	for (int i = 0; i < 8; i++)
	{
		output <<= 32;
		output |= Hashes[i].to_ulong();

	}
	output <<= 256;
	return output;
}
void Sha256::reset_hashes()
{
	Hashes[0] = 0x6a09e667;
	Hashes[1] = 0xbb67ae85;
	Hashes[2] = 0x3c6ef372;
	Hashes[3] = 0xa54ff53a;
	Hashes[4] = 0x510e527f;
	Hashes[5] = 0x9b05688c;
	Hashes[6] = 0x1f83d9ab;
	Hashes[7] = 0x5be0cd19;
	
}








