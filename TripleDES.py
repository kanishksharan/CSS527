
import sys
import os
import hashlib
import binascii

class userInputs:

	locationEncryptFile = os.getcwd()
	print ("In order to perform a successful run, provide the following as input parameters: \n",
		"1. Enter the name of the file to be encrypted. Make sure the file's location is: %s" %(locationEncryptFile),"\n",
		"2. Enter the password (key)")

	plaintextFileName = str (input ())
	userPassword = str (input())

	# Creating the method to hash password into SHA256 algorithm keys

	def genKey(self):

		encodedPassword = userInputs.userPassword.encode ('utf-8')
		hashPassword = hashlib.sha256 (encodedPassword).hexdigest() 

		'''User given pass converted to SHA256 bit hexadecimal.
		 This results is always 64 digits in length'''

		# Now converting hexadecimal value to binary
		# Each hexadecimal digit translates to 4 binary digits

		hashPasswordSize = len(hashPassword) * 4
		finalPassword = (bin(int(hashPassword,16))[2:]).zfill(hashPasswordSize)
		
		# Creating 3 keys to implement 3DES algorithm
		# 0-55 bits = Key1
		# 55-109 bits = Key2
		# 110-165 bits = key3
		key1 = finalPassword[0:56]
		key2 = finalPassword[56:112]
		key3 = finalPassword[114:170]

		# Now storing these 3 keys in a file called, "genKey.txt"
		filegenKey = open ("genKey.txt","w")
		filegenKey.write (str(key1) + "\n")
		filegenKey.write (str(key2) + "\n")
		filegenKey.write (str(key3) + "\n")

		filegenKey.close()

class msgEncrypt(userInputs): # This class will perform all the encryption operations

	# Accept the contents of the file to be encrypted

	filePlainText = open (userInputs.plaintextFileName,"r")
	copyPlaintext = ("\n".join(filePlainText.readlines()))
	filePlainText.close()

	tempPlaintext = ""
	paddedPlainText = ""
	concatPlainText = ""

	for bits in copyPlaintext:
		tempPlaintext = bin(ord(bits)) # Plaintext converted to binary
		paddedPlainText = tempPlaintext[2:].zfill(8)
		concatPlainText += paddedPlainText

	# Now divide the contents of file into 64-bits chunks or block ciphers

	print (len(concatPlainText))
	print (len(copyPlaintext))

	while (len(concatPlainText)%64 != 0):
		concatPlainText += "0" * (len(concatPlainText)%64)

	print (concatPlainText)
	print (len(concatPlainText))

	# For every block of 64-bits plaintext, there must be an unique IV

	totalPlainTextBlocks = int(len(concatPlainText)/64) # Gives the totl number of 64-bits Plain Text blocks required
	IV_List = list()

	# Now generating 64-bit Initialization Vector (IV)
	# First generating 8-bytes i.e. 8*8 = 64-bits of random number

	for iteration in range (0,totalPlainTextBlocks):
		randomIV = os.urandom(8)
		randomIVHex = binascii.hexlify(randomIV)
		ivhexSize = len(randomIVHex)
		IV = (bin(int(randomIVHex,16))[2:]).zfill(64)
		IV_List.append(IV)

	print (IV_List)
	print (len(IV_List))

	def IP(self):

		tableIP = [58,50,42,34,26,18,10,2,
				   60,52,44,36,28,20,12,4,
				   62,54,46,38,30,22,14,6,
				   64,56,48,40,32,24,16,8,
				   57,49,41,33,25,17,9,1,
				   59,51,43,35,27,19,11,3,
				   61,53,45,37,29,21,13,5,
				   63,55,47,39,31,23,15,7,
				   ]

		plaintextBlock = list()
		tempBlock = ""
		iter_counter = 0
		leftBits = 0
		rightBits = 0

		for element in msgEncrypt.IV_List: # Iterate through each IV from the IV list: IV_List
			for position in tableIP: # Bit shifting
				plaintextBlock.append(element[position-1])

				if len(plaintextBlock) == 64:
					iter_counter += 1
					print("I have the IV number: %d"%(iter_counter))
					tempBlock = "".join(plaintextBlock)
					plaintextBlock.clear()
					print (tempBlock)

					# Now divind the 64-bits input into L and R, each of 32-bits
					leftBits = tempBlock[0:32]
					rightBits = tempBlock[32:64]

					print (leftBits,len(leftBits))
					print (rightBits,len(rightBits))

					# Implementing E-box: Extending the R-32bits to 48-bits

					eBox = [32,		1,	2,	3,		4,		5,
                           4,     5,    6,     7,     8,    9,
                          8,     9,   10,    11,    12,   13,
                         12,    13,   14,    15,    16,   17,
                         16,    17,   18,    19,    20,   21,
                         20,    21,   22,    23,    24,   25,
                         24,    25,   26,    27,    28,  29,
                         28,    29,   30,    31,    32,    1
						]
					eboxRightBits = list()
					streboxRight = ""

					for eposition in eBox:
						eboxRightBits.append(rightBits[eposition-1])
						streboxRight = "".join(eboxRightBits)

					# Now Key1 XoR streboxRight
					getKey1 = open("genKey.txt","r")
					keyE1 = "".join(getKey1.readline())

					print (streboxRight, len(streboxRight))
					print (keyE1,len(keyE1))
					xorRK = int(streboxRight)^int(keyE1)
					print(xorRK)




					# print (eboxRightBits)	
					# print (streboxRight)	

		




	

		


c1 = msgEncrypt()
c1.genKey()
c1.IP()
