#include <iostream>
#include "HMac.h"
#include <fstream>





int main(int argc,char**argv)
{
	

	Hmac hMac(argv[1]);
	
	bitset<256> hmacBits = hMac.apply_Hmac(argv[2]);

	FILE* output = fopen(argv[3], "w");
	int end = 256 / 4;
	for (int i = end - 1; i >= 0; i--)
	{
		unsigned int  print = 0;
		for (int j = 3; j >= 0; j--)
		{
			print <<= 1;
			if (hmacBits.test(i * 4 + j))
			{

				print |= 1;
			}

		}
	
		if (print < 10)
		{
			fprintf(output, "%d", print);
		}
		else
		{
			fprintf(output, "%c", (65 + (print % 10)));
		}
	}
	
	fclose(output);

	


}
