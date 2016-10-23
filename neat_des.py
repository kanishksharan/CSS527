import sys
import os
import hashlib
import binascii

locationEncryptFile = os.getcwd()
print("In order to perform a successful run, provide the following as input parameters: \n",
      "Or else enter the absolute path of the file : \n",
      "1. Enter the name of the file to be encrypted. Make sure the file's location is: %s" % (locationEncryptFile),
      "\n",
      "2. Enter the password (key)")

plaintextFileName = str(input())
userPassword = str(input())

'''User given pass converted to SHA256 bit hexadecimal.
 This results is always 64 digits in length'''

encodedPassword = userPassword.encode('utf-8')
hashPassword = hashlib.sha256(encodedPassword).hexdigest()

# Now converting hexadecimal value to binary
# Each hexadecimal digit translates to 4 binary digits

hashPasswordSize = len(hashPassword) * 4
finalPassword = (bin(int(hashPassword, 16))[2:]).zfill(hashPasswordSize)

# Creating 3 keys to implement 3DES algorithm
# 0-55 bits = Key1
# 55-109 bits = Key2
# 110-165 bits = key3
key1 = finalPassword[0:64]
key2 = finalPassword[64:128]
key3 = finalPassword[128:192]

# print ("key1",len(key1))
# print ("key2",len(key2))
# print ("key3",len(key3))


# Writing the keys to the file
filegenKey = open("genKey.txt", "w")
filegenKey.write(str(key1) + "\n")
filegenKey.write(str(key2) + "\n")
filegenKey.write(str(key3) + "\n")
filegenKey.close()  # Reading hashed keys from the file

hashKey1 = ""
hashKey2 = ""
hashKey3 = ""
iteration_counter = 0
lstDecrypt = list()



# Reading the 3 hashed keys from the file one by one and storing them in the "hashkey" variables
with open("genKey.txt") as genKey:
    for lines in genKey:

        if iteration_counter == 0:
            hashKey1 = lines.strip()

        elif iteration_counter == 1:
            hashKey2 = lines.strip()

        elif iteration_counter == 2:
            hashKey3 = lines.strip()

        iteration_counter += 1

genKey.close()

# Declaring global variables
roundKey1 = ""
roundKey2 = ""
roundKey3 = ""
roundKey4 = ""
roundKey5 = ""
roundKey6 = ""
roundKey7 = ""
roundKey8 = ""
roundKey9 = ""
roundKey10 = ""
roundKey11 = ""
roundKey12 = ""
roundKey13 = ""
roundKey15 = ""
roundKey14 = ""
roundKey16 = ""
lstRoundKey = list()
binPlainText = ""
lstIV = list()
feedEBox = ""
sBlocks = ""
LplusR = ""
pxor = ""
lstPlainText = list()
lstCipher = list ()

strLeftBits = ""
xorRK = ""
lstBlocks = list()
lstPBox = list()
lstFeeder = list()

# PKCS 5

def pkcs5():
    global binPlainText
    # Reading plaintext from the file
    tempPlaintext = ""
    paddedPlainText = ""
    concatPlainText = ""
    filePlainText = open("inputFile.txt", "r")
    copyPlaintext = ("\n".join(filePlainText.readlines()))
    filePlainText.close()
    # Converting plaintext to Hexademical
    filePlainText = open("inputFile.txt", "r")
    copyPlaintext = ("\n".join(filePlainText.readlines()))
    filePlainText.close()
    # Converting plaintext to Hexademical
    for bits in copyPlaintext:
        tempPlaintext = bits.encode('utf-8')
        paddedPlainText = binascii.hexlify(tempPlaintext)
        concatPlainText += (paddedPlainText).decode("utf-8")

    # print(concatPlainText, len(concatPlainText))
    numbers = {0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9", 10: "10", 11: "11", 12: "12",
               13: "13", 14: "14", 15: "15", 16: "16", 17: "17", 18: "18",
               19: "19", 20: "20", 21: "21", 22: "22", 23: "23", 24: "24", 25: "25", 26: "26", 27: "27", 28: "28", 29: "29",
               30: "30", 31: "31", 32: "32", 33: "33", 34: "34", 35: "35",
               36: "36", 37: "37", 38: "38", 39: "39", 40: "40", 41: "41", 42: "42", 43: "43", 44: "44", 45: "45", 46: "46",
               47: "47", 48: "48", 49: "49", 50: "50", 51: "51", 52: "52",
               53: "53", 54: "54",
               55: "55", 56: "56", 57: "57", 58: "58", 59: "59", 60: "60", 61: "61", 62: "62", 63: "63", 64: "64"}

    if len(concatPlainText) % 64 != 0:
        val = len(concatPlainText) / 64
        actual_val = int(val + 1)
        padding = (64 * actual_val - len(concatPlainText))
        times = int(padding / 2)
        concatPlainText += numbers.get(padding) * times
        intPlainText = int(concatPlainText, 16)
        binPlainText = bin (intPlainText)[2:].zfill(len(concatPlainText)*4)
    else:
        intPlainText = int(concatPlainText, 16)
        binPlainText = bin (intPlainText)[2:].zfill(len(concatPlainText)*4)

    return binPlainText

pkcs5()




def PlaintextChunks(plaintext):
    global lstPlainText
    f = 0
    l = 64
    lst = list()

    while l <= len(plaintext):
        for i in range(0, 1):
            lst.append(plaintext[f:l])
        f += 64
        l += 64
        strng = "".join(lst)
        lstPlainText.append(strng)
        lst.clear()

    return lstPlainText
PlaintextChunks(binPlainText)


# Generating Initialization Vector
totalPlainTextBlocks = int(len(binPlainText) / 64)
randomIV = os.urandom(8)

for iteration in range(0, totalPlainTextBlocks):
    randomIVHex = binascii.hexlify(randomIV)
    ivhexSize = len(randomIVHex)
    IV = (bin(int(randomIVHex, 16))[2:]).zfill(64)
    lstIV.append(IV)
    IV += bin(1)
    print (lstIV)



def leftCircularShift(strBinary, j):
    iterator = [x for x in range(0, len(strBinary))]
    iteratorLst = list(strBinary)
    shift = [y for y in range(0, len(strBinary))]
    counter = 0
    if j in (1, 2, 9, 16):
        for i in iteratorLst:
            position = iteratorLst.index(i, 0)
            shift[position - 1] = i
            iteratorLst[counter] = 'x'
            counter += 1

        strShift = "".join(shift)

    if j in (3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15):
        for i in iteratorLst:
            position = iteratorLst.index(i, 0)
            shift[position - 2] = i
            iteratorLst[counter] = 'x'
            counter += 1

        strShift = "".join(shift)

    return strShift

def SecondPermutation(shiftkey):
    PC2 = [14, 17, 11, 24, 1, 5
        , 3, 28, 15, 6, 21, 10
        , 23, 19, 12, 4, 26, 8
        , 16, 7, 27, 20, 13, 2
        , 41, 52, 31, 37, 47, 55
        , 30, 40, 51, 45, 33, 48
        , 44, 49, 39, 56, 34, 53
        , 46, 42, 50, 36, 29, 32]

    iteration_counter = 0
    keyLst = list()
    for position in PC2:

        if position > 48:
            pass

        else:
            if iteration_counter < 48:
                keyLst.append(shiftkey[position - 1])
                iteration_counter += 1

    key = "".join(keyLst)
    return key

def roundKeyGen(key1):
    # Declaring global variables inside the function
    global roundKey1
    global roundKey2
    global roundKey3
    global roundKey4
    global roundKey5
    global roundKey6
    global roundKey7
    global roundKey8
    global roundKey9
    global roundKey10
    global roundKey11
    global roundKey12
    global roundKey13
    global roundKey14
    global roundKey15
    global roundKey16
    global lstRoundKey

    initialKey = key1
    passwordLst = list()

    PC1 = [57, 49, 41, 33, 25, 17, 9
        , 1, 58, 50, 42, 34, 26, 18
        , 10, 2, 59, 51, 43, 35, 27
        , 19, 11, 3, 60, 52, 44, 36
        , 63, 55, 47, 39, 31, 23, 15
        , 7, 62, 54, 46, 38, 30, 22
        , 14, 6, 61, 53, 45, 37, 29
        , 21, 13, 5, 28, 20, 12, 4]


    for position in PC1:
        passwordLst.append(initialKey[position - 1])

    password = "".join(passwordLst)
    # Split the password in half (28-bits)
    passwordC = password[:28]
    passwordD = password[28:56]

    for iteration in range(1, 17):

        if iteration in (1, 2, 9, 16):

            if iteration == 1:
                cShift1 = leftCircularShift(passwordC, iteration)
                dShift1 = leftCircularShift(passwordD, iteration)
                shiftKey1 = str(cShift1 + dShift1)
                roundKey1 = SecondPermutation(shiftKey1)

            if iteration == 2:
                cShift2 = leftCircularShift(cShift1, iteration)
                dShift2 = leftCircularShift(dShift1, iteration)
                shiftKey2 = str(cShift2 + dShift2)
                roundKey2 = SecondPermutation(shiftKey2)

            if iteration == 9:
                cShift9 = leftCircularShift(cShift8, iteration)
                dShift9 = leftCircularShift(dShift8, iteration)
                shiftKey9 = str(cShift9 + dShift9)
                roundKey9 = SecondPermutation(shiftKey9)

            if iteration == 16:
                cShift16 = leftCircularShift(cShift15, iteration)
                dShift16 = leftCircularShift(dShift15, iteration)
                shiftKey16 = str(cShift16 + dShift16)
                roundKey16 = SecondPermutation(shiftKey16)

        if iteration in (3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15):

            cShift3 = leftCircularShift(cShift2, iteration)
            cShift4 = leftCircularShift(cShift3, iteration)
            cShift5 = leftCircularShift(cShift4, iteration)
            cShift6 = leftCircularShift(cShift5, iteration)
            cShift7 = leftCircularShift(cShift6, iteration)
            cShift8 = leftCircularShift(cShift7, iteration)

            dShift3 = leftCircularShift(dShift2, iteration)
            dShift4 = leftCircularShift(dShift3, iteration)
            dShift5 = leftCircularShift(dShift4, iteration)
            dShift6 = leftCircularShift(dShift5, iteration)
            dShift7 = leftCircularShift(dShift6, iteration)
            dShift8 = leftCircularShift(dShift7, iteration)

            if iteration == 10:
                cShift10 = leftCircularShift(cShift9, iteration)
                cShift11 = leftCircularShift(cShift10, iteration)
                cShift12 = leftCircularShift(cShift11, iteration)
                cShift13 = leftCircularShift(cShift12, iteration)
                cShift14 = leftCircularShift(cShift13, iteration)
                cShift15 = leftCircularShift(cShift14, iteration)

                dShift10 = leftCircularShift(dShift9, iteration)
                dShift11 = leftCircularShift(dShift10, iteration)
                dShift12 = leftCircularShift(dShift11, iteration)
                dShift13 = leftCircularShift(dShift12, iteration)
                dShift14 = leftCircularShift(dShift13, iteration)
                dShift15 = leftCircularShift(dShift14, iteration)

                shiftKey3 = str(cShift3 + dShift3)
                roundKey3 = SecondPermutation(shiftKey3)

                shiftKey4 = str(cShift4 + dShift4)
                roundKey4 = SecondPermutation(shiftKey4)

                shiftKey5 = str(cShift5 + dShift5)
                roundKey5 = SecondPermutation(shiftKey5)

                shiftKey6 = str(cShift6 + dShift6)
                roundKey6 = SecondPermutation(shiftKey6)

                shiftKey7 = str(cShift7 + dShift7)
                roundKey7 = SecondPermutation(shiftKey7)

                shiftKey8 = str(cShift8 + dShift8)
                roundKey8 = SecondPermutation(shiftKey8)

                shiftKey10 = str(cShift10 + dShift10)
                roundKey10 = SecondPermutation(shiftKey10)

                shiftKey11 = str(cShift11 + dShift11)
                roundKey11 = SecondPermutation(shiftKey11)

                shiftKey12 = str(cShift12 + dShift12)
                roundKey12 = SecondPermutation(shiftKey12)

                shiftKey13 = str(cShift13 + dShift13)
                roundKey13 = SecondPermutation(shiftKey13)

                shiftKey14 = str(cShift14 + dShift14)
                roundKey14 = SecondPermutation(shiftKey14)

                shiftKey15 = str(cShift15 + dShift15)
                roundKey15 = SecondPermutation(shiftKey15)
    lstRoundKey = [roundKey1, roundKey2, roundKey3, roundKey4, roundKey5, roundKey6, roundKey7, roundKey8, roundKey9, roundKey10, roundKey11, roundKey12, roundKey13, roundKey14, roundKey15, roundKey16]

    return roundKey1, roundKey2, roundKey3, roundKey4, roundKey5, roundKey6, roundKey7, roundKey8, roundKey9, roundKey10, roundKey11, roundKey12, roundKey13, roundKey14, roundKey15, roundKey16





# This method performs the initial permutations

def IP(iv):
    global feedEBox
    tableIP = [58, 50, 42, 34, 26, 18, 10, 2,
          60, 52, 44, 36, 28, 20, 12, 4,
          62, 54, 46, 38, 30, 22, 14, 6,
          64, 56, 48, 40, 32, 24, 16, 8,
          57, 49, 41, 33, 25, 17, 9, 1,
          59, 51, 43, 35, 27, 19, 11, 3,
          61, 53, 45, 37, 29, 21, 13, 5,
          63, 55, 47, 39, 31, 23, 15, 7]

    tempShift = list()
    for position in tableIP:  # Bit shifting

        tempShift.append(iv[position - 1])

    feedEBox = "".join(tempShift)

    return feedEBox

def EBox(l, r, loopcounter):
    strLeftBits = l

    eboxRightBits = list()
    leftBits = ""
    global lstRoundKey
    global xorRK

    Ebox = [32, 1, 2, 3, 4, 5,
            4, 5, 6, 7, 8, 9,
            8, 9, 10, 11, 12, 13,
            12, 13, 14, 15, 16, 17,
            16, 17, 18, 19, 20, 21,
            20, 21, 22, 23, 24, 25,
            24, 25, 26, 27, 28, 29,
            28, 29, 30, 31, 32, 1]

    # Now divide the 64-bits input into L and R, each of 32-bits
    # leftBits = ip[0:32]
    # rightBits = ip[32:64]
    currentRoundKey = lstRoundKey[loopcounter]# Fetching the round key

    for eposition in Ebox:
        eboxRightBits.append(r[eposition - 1])
    stringRBits = "".join(eboxRightBits)  # Now we XoR stringRBits ^ Key1

    intRBits = int(stringRBits, 2)
    keyX = int(currentRoundKey, 2)
    intxorRK = intRBits ^ keyX
    xorRK = bin(intxorRK)[2:].zfill(48)

    return xorRK, strLeftBits


# This function performs the xbox
def SBox(xorRK):  # This function performs the tedious S-Box implementation

    global sBlocks
    lstxorRK = xorRK
    # print (lstxorRK)

    sBox1 = [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7,
             0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8,
             4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0,
             15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]

    sBox2 = [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10,
             3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5,
             0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15,
             13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]

    sBox3 = [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8,
             13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1,
             13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7,
             1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]

    sBox4 = [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15,
             13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9,
             10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4,
             3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]

    sBox5 = [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9,
             14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6,
             4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14,
             11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]

    sBox6 = [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11,
             10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8,
             9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6,
             4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]

    sBox7 = [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1,
             13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6,
             1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2,
             6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]

    sBox8 = [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7,
             1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2,
             7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8,
             2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]

    # Create 8 2-D Arrays to store the table values
    row = 4
    col = 16

    table1 = [[0 for c in range(col)] for r in range(row)]
    table2 = [[0 for c in range(col)] for r in range(row)]
    table3 = [[0 for c in range(col)] for r in range(row)]
    table4 = [[0 for c in range(col)] for r in range(row)]
    table5 = [[0 for c in range(col)] for r in range(row)]
    table6 = [[0 for c in range(col)] for r in range(row)]
    table7 = [[0 for c in range(col)] for r in range(row)]
    table8 = [[0 for c in range(col)] for r in range(row)]

    i = 0
    for r in range(0, 4):
        for c in range(0, 16):
            table1[r][c] = sBox1[i]
            i += 1
            continue

    # Filling elements in table2 from sBox2
    i = 0
    for r in range(0, 4):
        for c in range(0, 16):
            table2[r][c] = sBox2[i]
            i += 1
            continue

    # Filling elements in table3 from sBox3
    i = 0
    for r in range(0, 4):
        for c in range(0, 16):
            table3[r][c] = sBox3[i]
            i += 1
            continue

    # Filling elements in table4 from sBox4
    i = 0
    for r in range(0, 4):
        for c in range(0, 16):
            table4[r][c] = sBox4[i]
            i += 1
            continue

    # Filling elements in table5 from sBox5
    i = 0
    for r in range(0, 4):
        for c in range(0, 16):
            table5[r][c] = sBox5[i]
            i += 1
            continue

    # Filling elements in table6 from sBox6
    i = 0
    for r in range(0, 4):
        for c in range(0, 16):
            table6[r][c] = sBox6[i]
            i += 1
            continue

    # Filling elements in table7 from sBox7
    i = 0
    for r in range(0, 4):
        for c in range(0, 16):
            table7[r][c] = sBox7[i]
            i += 1
            continue

    # Filling elements in table8 from sBox8
    i = 0
    for r in range(0, 4):
        for c in range(0, 16):
            table8[r][c] = sBox8[i]
            i += 1
            continue  # Divide the 48-bits into 8 parts of 6-bits each

    block1 = lstxorRK[0:6]
    block2 = lstxorRK[6:12]
    block3 = lstxorRK[12:18]
    block4 = lstxorRK[18:24]
    block5 = lstxorRK[24:30]
    block6 = lstxorRK[30:36]
    block7 = lstxorRK[36:42]
    block8 = lstxorRK[42:48]

    left1, right1, middle1 = block1[0], block1[-1], block1[1:-1]
    outer1 = int(left1 + right1, 2)
    center1 = int(middle1, 2)

    left2, right2, middle2 = block2[0], block2[-1], block2[1:-1]
    outer2 = int(left2 + right2, 2)
    center2 = int(middle2, 2)

    left3, right3, middle3 = block3[0], block3[-1], block3[1:-1]
    outer3 = int(left3 + right3, 2)
    center3 = int(middle3, 2)

    left4, right4, middle4 = block4[0], block4[-1], block4[1:-1]
    outer4 = int(left4 + right4, 2)
    center4 = int(middle4, 2)

    left5, right5, middle5 = block5[0], block5[-1], block5[1:-1]
    outer5 = int(left5 + right5, 2)
    center5 = int(middle5, 2)

    left6, right6, middle6 = block6[0], block6[-1], block6[1:-1]
    outer6 = int(left6 + right6, 2)
    center6 = int(middle6, 2)

    left7, right7, middle7 = block7[0], block7[-1], block7[1:-1]
    outer7 = int(left7 + right7, 2)
    center7 = int(middle7, 2)

    left8, right8, middle8 = block8[0], block8[-1], block8[1:-1]
    outer8 = int(left8 + right8, 2)
    center8 = int(middle8, 2)

    b1 = bin(table1[outer1][center1])[2:].zfill(4)
    b2 = bin(table2[outer2][center2])[2:].zfill(4)
    b3 = bin(table3[outer3][center3])[2:].zfill(4)
    b4 = bin(table4[outer4][center4])[2:].zfill(4)
    b5 = bin(table5[outer5][center5])[2:].zfill(4)
    b6 = bin(table6[outer6][center6])[2:].zfill(4)
    b7 = bin(table7[outer7][center7])[2:].zfill(4)
    b8 = bin(table8[outer8][center8])[2:].zfill(4)

    cBlocks = list([b1, b2, b3, b4, b5, b6, b7, b8])
    sBlocks = "".join(cBlocks)
    return sBlocks


#  This function performs PBox
def PBox(sBlocks, lstLeftBits):
    global lstBlocks
    global lstPBox
    global lstFeeder
    global pxor

    # print(lstLeftBits, len(lstLeftBits), len(lstLeftBits[12]))
    # print(lstBlocks, len(lstBlocks), len(lstBlocks[12]))

    tempPBox = list()
    strPBox = ""

    Pbox = [16, 7, 20, 21,
            29, 12, 28, 17,
            1, 15, 23, 26,
            5, 18, 31, 10,
            2, 8, 24, 14,
            32, 27, 3, 9,
            19, 13, 30, 6,
            22, 11, 4, 25]

    for position in Pbox:
        tempPBox.append(sBlocks[position - 1])
    strPBox = "".join(tempPBox)

    intpbox = int(strPBox, 2)
    intblocks = int(lstLeftBits, 2)
    pxor = bin(intpbox ^ intblocks)[2:].zfill(32)

    return pxor

def Encrypt():
    global feedEBox
    global LplusR
    global key1
    global lstIV
    global pxor
    global xorRK
    global sBlocks
    global binPlainText
    global lstPlainText
    global lstCipher

    loopcounter = 0
    EncryptExit = ""
    tempFP = list()

    FinalCipher = ""
    cipher1 = ""
    iterator = 0
    roundKeyGen(key1)
    # PlaintextChunks(binPlainText)

    FP = [40, 8, 48, 16, 56, 24, 64, 32
        , 39, 7, 47, 15, 55, 23, 63, 31
        , 38, 6, 46, 14, 54, 22, 62, 30
        , 37, 5, 45, 13, 53, 21, 61, 29
        , 36, 4, 44, 12, 52, 20, 60, 28
        , 35, 3, 43, 11, 51, 19, 59, 27
        , 34, 2, 42, 10, 50, 18, 58, 26
        , 33, 1, 41, 9, 49, 17, 57, 25]

    for iv in lstIV:
        IP(iv)
        LplusR = feedEBox
        # c = lstIV.index(iv)
        while loopcounter < 16:
            leftBits = LplusR[0:32]
            rightBits = LplusR[32:64]
            EBox(leftBits, rightBits, loopcounter)
            SBox(xorRK)
            PBox(sBlocks, leftBits)
            LplusR = str(rightBits) + str(pxor)

            if loopcounter == 15:
                for position in FP:
                    tempFP.append(LplusR[position - 1])
                EncryptExit = "".join(tempFP)
            loopcounter += 1

        cipher1 = lstPlainText[iterator]

        intCipher = int(cipher1, 2)
        intEncryptExit = int(EncryptExit, 2)
        FinalCipher = bin(intCipher ^ intEncryptExit)[2:].zfill(64)
        iterator += 1
        lstCipher.append(FinalCipher)
        # lstCipher.append(hex(int(FinalCipher,2)))
        # print (lstCipher)
        # print (len(lstCipher))
    return lstCipher

Encrypt()

def Decrypt():
    global feedEBox
    global LplusR
    global key1
    global lstIV
    global pxor
    global xorRK
    global sBlocks
    global binPlainText
    global lstPlainText
    global lstCipher
    global lstDecrypt
    print ("Decrypt Start")
    loopcounter = 15
    EncryptExit = ""
    tempFP = list()

    FinalCipher = ""
    cipher1 = ""
    iterator = len(lstCipher)-1
    # roundKeyGen(key1)
    # PlaintextChunks(binPlainText)

    FP = [40, 8, 48, 16, 56, 24, 64, 32
        , 39, 7, 47, 15, 55, 23, 63, 31
        , 38, 6, 46, 14, 54, 22, 62, 30
        , 37, 5, 45, 13, 53, 21, 61, 29
        , 36, 4, 44, 12, 52, 20, 60, 28
        , 35, 3, 43, 11, 51, 19, 59, 27
        , 34, 2, 42, 10, 50, 18, 58, 26
        , 33, 1, 41, 9, 49, 17, 57, 25]

    for i in range(len(lstCipher)-1,-1,-1):
        IP(lstCipher[i])
        LplusR = feedEBox
        # c = lstIV.index(iv)
        while loopcounter >= 0:
            leftBits = LplusR[0:32]
            rightBits = LplusR[32:64]
            EBox(leftBits, rightBits, loopcounter)
            SBox(xorRK)
            PBox(sBlocks, leftBits)
            LplusR = str(rightBits) + str(pxor)

            if loopcounter == 0:
                for position in FP:
                    tempFP.append(LplusR[position - 1])
                EncryptExit = "".join(tempFP)
            loopcounter -= 1

        cipher1 = lstCipher[iterator]

        intCipher = int(cipher1, 2)
        intEncryptExit = int(EncryptExit, 2)
        FinalCipher = bin(intCipher ^ intEncryptExit)[2:].zfill(64)
        iterator -= 1
        lstDecrypt.append(FinalCipher)
        # lstCipher.append(hex(int(FinalCipher,2)))
        # print (lstDecrypt)
        # print (len(lstDecrypt))

    return lstCipher
Decrypt()

print ("Chunks",lstPlainText,len(lstPlainText[2]))
print ("Cipher",lstCipher, len(lstCipher))
print ("Decrypt",lstDecrypt, len(lstDecrypt))
