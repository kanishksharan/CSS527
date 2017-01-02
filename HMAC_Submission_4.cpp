#include "HMac.h"
#include "sha256.h"

int get_file_size(std::string filePath)
{
	ifstream file(filePath, ios::binary | ios::ate);
	int length = file.tellg();
	file.close();
	return length;
}



void print_bitset(string prefix, bitset<256> message)
{
	cout << prefix << endl;
	int end = 256 / 4;
	for (int i = end - 1; i >= 0; i--)
	{
		unsigned int  print = 0;
		for (int j = 3; j >= 0; j--)
		{
			print <<= 1;
			if (message.test(i * 4 + j))
			{

				print |= 1;
			}

		}
		if (print < 10)
		{
			printf("%d", print);
		}
		else
		{
			printf("%c", (65 + (print % 10)));
		}
	}
	cout << endl;
}

void print_bitset_512(string prefix, bitset<512> message)
{
	cout << prefix << endl;
	int end = 512 / 4;
	for (int i = end - 1; i >= 0; i--)
	{
		unsigned int  print = 0;
		for (int j = 3; j >= 0; j--)
		{
			print <<= 1;
			if (message.test(i * 4 + j))
			{

				print |= 1;
			}

		}
		if (print < 10)
		{
			printf("%d", print);
		}
		else
		{
			printf("%c", (65 + (print % 10)));
		}
	}
	cout << endl;
}

Hmac::Hmac(const char* key_path)
{

	int readBytes = 0;
	int keySizeBits = get_file_size(key_path) * 8;
	FILE* file = fopen(key_path, "rb");
	if (!file)
	{
		printf("Error opening key file\nApplication shutdown!!!\n");
		system("PAUSE");
		exit(0);
	}
	int rc = 0;
	
	byte buffer[] = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };

	
	
	if (keySizeBits <= BLOCK_SIZE_BITS)
	{
		while (rc = fread(buffer, sizeof(byte), 64, file))
		{
			readBytes += rc;
			for (int i = 0; i < rc; i++)
			{
				key <<= 8;
				key |= buffer[i];
			}

		}	
		key <<= (BLOCK_SIZE_BITS - (readBytes * 8));
		
	}
	
	else 
	{
		Sha256 sha256;
		while (rc = fread(buffer, sizeof(byte), 64, file))
		{
			readBytes += rc;
			for (int i = 0; i < rc; i++)
			{
				key <<= 8;
				key |= buffer[i];
			}
			
			if (readBytes * 8 == keySizeBits)
			{
				//last block
				if (rc == 64)
				{

					sha256.hash_chunk(key);

					bitset<512> padChunk = sha256.apply_fresh_padding(keySizeBits + 512);
					sha256.hash_chunk(padChunk);
				}
				else if ((rc * 8) <= (BLOCK_SIZE_BITS - (66)))
				{

					key = sha256.apply_last_chunk_padding(key, (rc * 8),keySizeBits + 512);
					sha256.hash_chunk(key);

				}
				else
				{

					pair<bitset<512>, bitset<512>> lastAndSpilled = sha256.apply_chunk_and_fresh_padding(key, (rc * 8), keySizeBits + 512);//*8 to convert from bytes to bits+ 512 for the k xor ipad
					sha256.hash_chunk(lastAndSpilled.first);
					sha256.hash_chunk(lastAndSpilled.second);
				}
			}
			else{
				sha256.hash_chunk(key);
				key.reset();
			}

		}
	
		key = sha256.get_current_hash_512();
	}
	
	fclose(file);
	
	size_t n = BLOCK_SIZE_BITS / 8;
	size_t iPadMask = 0x36; /*00110110*/
	size_t oPadMask = 0x5C; /*01011100*/
	for (int i = 0; i < n; i++)
	{
		i_pad <<= 8;
		o_pad <<= 8;
		i_pad |= iPadMask;
		o_pad |= oPadMask;
	}
	
}

bitset<256> Hmac::hash_concat_key_xor_ipad_message(const char* message_path)
{
	
	Sha256 sha;
	
	sha.hash_chunk((key^i_pad));

	
	int fileSize = get_file_size(message_path);
	int readBytes = 0;
	FILE* file = fopen(message_path, "rb");
	if (!file)
	{
		printf("Error opening file\nApplication shutdown!!!\n");
		system("PAUSE");
		exit(0);
	}
	
	byte buffer[] = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 };
	int rc = 0;
	int blockSizeBytes = BLOCK_SIZE_BITS / 8;

	
	int x = 0;
	
	while (rc = fread(buffer, sizeof(byte), blockSizeBytes, file))
	{
		readBytes += rc;
		bitset<512> block(0);
		for (int i = 0; i < rc; i++)
		{
			block <<= 8;
			block |= buffer[i];
		}
		if (readBytes == fileSize)
		{
			
			if (rc == blockSizeBytes)
			{
				
				sha.hash_chunk(block);
				
				bitset<512> padChunk = sha.apply_fresh_padding((fileSize * 8)+512);
				sha.hash_chunk(padChunk);
			}
			else if ((rc * 8) <= (BLOCK_SIZE_BITS - (66))) 
			{
				
				block = sha.apply_last_chunk_padding(block, (rc * 8), (fileSize * 8) + 512);
				sha.hash_chunk(block);
				
			}
			else
			{
				
				pair<bitset<512>, bitset<512>> lastAndSpilled = sha.apply_chunk_and_fresh_padding(block, (rc * 8), (fileSize * 8) +512);//*8 to convert from bytes to bits+ 512 for the k xor ipad
				sha.hash_chunk(lastAndSpilled.first);
				sha.hash_chunk(lastAndSpilled.second);
			}
		}
		else
		{
			
			sha.hash_chunk(block);
			block.reset();
		}
	}
	fclose(file);
	
	return sha.get_current_hash();

}

bitset<256> Hmac::hash_concat_key_xor_opad_first_hash(bitset<256> hash)
{


	Sha256 sha;
	sha.hash_chunk(key^o_pad);
	
	bitset<512> hash512(0);
	//copy 256-bit hash to 512 bit hash
	for (int i = 0; i < 256; i++)
	{
		hash512[i] = hash[i];
	}
	
	bitset<512> paddedHash = sha.apply_last_chunk_padding(hash512, 256, 512 + 256);

	sha.hash_chunk(paddedHash);
	return sha.get_current_hash();
}
bitset<256> Hmac::apply_Hmac(const char* message_path)
{
	
	bitset<256> currMac = hash_concat_key_xor_ipad_message(message_path);
	print_bitset("First Hash output h((K xor IPad)|| message):", currMac);
	bitset<256> hMac = hash_concat_key_xor_opad_first_hash(currMac);
	print_bitset("Final HMac Output", hMac);
	return hMac;


}



