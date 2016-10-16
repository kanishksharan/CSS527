
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

	totalPlainTextBlocks = int(len(concatPlainText)/64) # Gives the total number of 64-bits Plain Text blocks required
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

					# Converting streBoxRight to int
					intEboxRight = int(streboxRight,2)

					# Now Key1 XoR streboxRight
					getKey1 = open("genKey.txt","r")
					keyE1 = "".join(getKey1.readline(56))
					intkeyE1 = int(keyE1,2) # Converting the key to int

					print (intEboxRight, len(streboxRight))
					print (intkeyE1,len(keyE1))
					xorRK = bin ((intEboxRight) ^ (intkeyE1))[2:].zfill(48)

					# Extract only 48-bits from the XoR output
					xorRK = xorRK[0:48]
					print(xorRK,len(xorRK))

					# Now implement S-Box
					# Divide the 48-bits into 8 parts of 6-bits each

					block1 = xorRK[0:6]
					block2 = xorRK[6:12]
					block3 = xorRK[12:18]
					block4 = xorRK[18:24]
					block5 = xorRK[24:30]
					block6 = xorRK[30:36]
					block7 = xorRK[36:42]
					block8 = xorRK[42:48]

					print (block1)
					print (block2)
					print (block3)
					print (block4)
					print (block5)
					print (block6)
					print (block7)
					print (block8)

					superBlock = list([block1,block2,block3,block4,block5,block6,block7,block8])
					print (superBlock)
					print (superBlock[1])

					# Creating the 8 S-Boxes

					sBox1 = (14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7,
					           0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8,
					           4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0,
					           15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13)


					sBox2 = (15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10,
					           3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5,
					           0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15,
					           13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9)

					sBox3 = (10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8,
					           13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1,
					           13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7,
					           1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12)

					sBox4 = (7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15,
					           13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9,
					           10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4,
					           3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14)


					sBox5 = (2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9,
					           14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6,
					           4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14,
					           11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3)

					sBox6 = (12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11,
					           10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8,
					           9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6,
					           4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13)

					sBox7 = (4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1,
					           13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6,
					           1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2,
					           6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12)

					sBox8 = (13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7,
					           1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2,
					           7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8,
					           2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11)

					# Create 8 2-D Arrays to store the table values
					row = 4
					col = 16

					table1 = [[0 for c in range (col)] for r in range (row)]
					table2 = [[0 for c in range (col)] for r in range (row)]
					table3 = [[0 for c in range (col)] for r in range (row)]
					table4 = [[0 for c in range (col)] for r in range (row)]
					table5 = [[0 for c in range (col)] for r in range (row)]
					table6 = [[0 for c in range (col)] for r in range (row)]
					table7 = [[0 for c in range (col)] for r in range (row)]
					table8 = [[0 for c in range (col)] for r in range (row)]

					# Filling elements in table1 from sBox1
					i = 0
					for r in range (0,4):
					    for c in range (0,16):
					        table1[r][c] = sBox1[i]
					        i += 1
					        continue

					# Filling elements in table2 from sBox2
					i = 0
					for r in range (0,4):
					    for c in range (0,16):
					        table2[r][c] = sBox2[i]
					        i += 1
					        continue

					# Filling elements in table3 from sBox3
					i = 0
					for r in range (0,4):
					    for c in range (0,16):
					        table3[r][c] = sBox3[i]
					        i += 1
					        continue

					# Filling elements in table4 from sBox4
					i = 0
					for r in range (0,4):
					    for c in range (0,16):
					        table4[r][c] = sBox4[i]
					        i += 1
					        continue

					# Filling elements in table5 from sBox5
					i = 0
					for r in range (0,4):
					    for c in range (0,16):
					        table5[r][c] = sBox5[i]
					        i += 1
					        continue

					# Filling elements in table6 from sBox6
					i = 0
					for r in range (0,4):
					    for c in range (0,16):
					        table6[r][c] = sBox6[i]
					        i += 1
					        continue

					# Filling elements in table7 from sBox7
					i = 0
					for r in range (0,4):
					    for c in range (0,16):
					        table7[r][c] = sBox7[i]
					        i += 1
					        continue

					# Filling elements in table8 from sBox8
					i = 0
					for r in range (0,4):
					    for c in range (0,16):
					        table8[r][c] = sBox8[i]
					        i += 1
					        continue

					left1,right1, middle1 = block1[0],block1[-1],block1[1:-1]
					outer1 = int(left1+right1,2)
					center1 = int(middle1,2)

					left2,right2, middle2 = block2[0],block2[-1],block2[1:-1]
					outer2 = int(left2+right2,2)
					center2 = int(middle2,2)

					left3,right3, middle3 = block3[0],block3[-1],block3[1:-1]
					outer3 = int(left3+right3,2)
					center3 = int(middle3,2)

					left4,right4, middle4 = block4[0],block4[-1],block4[1:-1]
					outer4 = int(left4+right4,2)
					center4 = int(middle4,2)

					left5,right5, middle5 = block5[0],block5[-1],block5[1:-1]
					outer5 = int(left5+right5,2)
					center5 = int(middle5,2)

					left6,right6, middle6 = block6[0],block6[-1],block6[1:-1]
					outer6 = int(left6+right6,2)
					center6 = int(middle6,2)

					left7,right7, middle7 = block7[0],block7[-1],block7[1:-1]
					outer7 = int(left7+right7,2)
					center7 = int(middle7,2)

					left8,right8, middle8 = block8[0],block8[-1],block8[1:-1]
					outer8 = int(left8+right8,2)
					center8 = int(middle8,2)

					b1 = bin(table1[outer1][center1])[2:].zfill(4)
					b2 = bin(table2[outer2][center2])[2:].zfill(4)
					b3 = bin(table3[outer3][center3])[2:].zfill(4)
					b4 = bin(table4[outer4][center4])[2:].zfill(4)
					b5 = bin(table5[outer5][center5])[2:].zfill(4)
					b6 = bin(table6[outer6][center6])[2:].zfill(4)
					b7 = bin(table7[outer7][center7])[2:].zfill(4)
					b8 = bin(table8[outer8][center8])[2:].zfill(4)

					print (outer1,center1)
					print (table1)
					print (b1)
					sBox32 = list ([b1,b2,b3,b4,b5,b6,b7,b8])
					print (sBox32)
					


					

	

		




	

		


c1 = msgEncrypt()
c1.genKey()
c1.IP()
