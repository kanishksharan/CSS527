#ifndef HMAC_H
#define HMAC_H
#define BLOCK_SIZE_BITS 512
#include <iostream>
#include <bitset>
#include <fstream>



using namespace std;


class Hmac
{
private:
	bitset<512> i_pad;
	bitset<512> o_pad;
	bitset<512> key;
	//concatenate k xor ipad with message and returns their hash
	bitset<256> hash_concat_key_xor_ipad_message(const char* message_path);

	//concatenate k xor opad with hash output from the previous function and return hash
	bitset<256> hash_concat_key_xor_opad_first_hash(bitset<256> hash);

	
public:
	//constructor that retrieves key and initialize ipad and opad
	Hmac(const char* key_path);

	//carry out HMac
	bitset<256> apply_Hmac(const char* message_path);

	

};
#endif
