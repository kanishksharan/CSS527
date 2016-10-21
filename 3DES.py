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


# This function performs the left circular shift


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


encodedPassword = userPassword.encode('utf-8')
hashPassword = hashlib.sha256(encodedPassword).hexdigest()

'''User given pass converted to SHA256 bit hexadecimal.
 This results is always 64 digits in length'''

# Now converting hexadecimal value to binary
# Each hexadecimal digit translates to 4 binary digits

hashPasswordSize = len(hashPassword) * 4
finalPassword = (bin(int(hashPassword, 16))[2:]).zfill(hashPasswordSize)

# Creating 3 keys to implement 3DES algorithm
# 0-55 bits = Key1
# 55-109 bits = Key2
# 110-165 bits = key3
key1 = finalPassword[0:56]
key2 = finalPassword[56:112]
key3 = finalPassword[114:170]

filegenKey = open("genKey.txt", "w")
filegenKey.write(str(key1) + "\n")
filegenKey.write(str(key2) + "\n")
filegenKey.write(str(key3) + "\n")

filegenKey.close()  # Reading hashed keys from the file
hashKey1 = ""
hashKey2 = ""
hashKey3 = ""
iteration_counter = 0

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
binPlainText = ""
lstIV = list()
feedEBox = list()
lstLeftBits = list()
lstxorRK = list()


# Creating the method to Generate 16 round keys

def roundKeyGen(keyx):
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

    initialKey = keyx
    passwordLst = list()

    tableIP = [58, 50, 42, 34, 26, 18, 10, 2,
               60, 52, 44, 36, 28, 20, 12, 4,
               62, 54, 46, 38, 30, 22, 14, 6,
               64, 56, 48, 40, 32, 24, 16, 8,
               57, 49, 41, 33, 25, 17, 9, 1,
               59, 51, 43, 35, 27, 19, 11, 3,
               61, 53, 45, 37, 29, 21, 13, 5,
               63, 55, 47, 39, 31, 23, 15, 7]

    for position in tableIP:
        if position > 56:
            pass

        else:
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
                roundKey1 = FinalPermutation(shiftKey1)

            if iteration == 2:
                cShift2 = leftCircularShift(cShift1, iteration)
                dShift2 = leftCircularShift(dShift1, iteration)
                shiftKey2 = str(cShift2 + dShift2)
                roundKey2 = FinalPermutation(shiftKey2)

            if iteration == 9:
                cShift9 = leftCircularShift(cShift8, iteration)
                dShift9 = leftCircularShift(dShift8, iteration)
                shiftKey9 = str(cShift9 + dShift9)
                roundKey9 = FinalPermutation(shiftKey9)

            if iteration == 16:
                cShift16 = leftCircularShift(cShift15, iteration)
                dShift16 = leftCircularShift(dShift15, iteration)
                shiftKey16 = str(cShift16 + dShift16)
                roundKey16 = FinalPermutation(shiftKey16)

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
                roundKey3 = FinalPermutation(shiftKey3)

                shiftKey4 = str(cShift4 + dShift4)
                roundKey4 = FinalPermutation(shiftKey4)

                shiftKey5 = str(cShift5 + dShift5)
                roundKey5 = FinalPermutation(shiftKey5)

                shiftKey6 = str(cShift6 + dShift6)
                roundKey6 = FinalPermutation(shiftKey6)

                shiftKey7 = str(cShift7 + dShift7)
                roundKey7 = FinalPermutation(shiftKey7)

                shiftKey8 = str(cShift8 + dShift8)
                roundKey8 = FinalPermutation(shiftKey8)

                shiftKey10 = str(cShift10 + dShift10)
                roundKey10 = FinalPermutation(shiftKey10)

                shiftKey11 = str(cShift11 + dShift11)
                roundKey11 = FinalPermutation(shiftKey11)

                shiftKey12 = str(cShift12 + dShift12)
                roundKey12 = FinalPermutation(shiftKey12)

                shiftKey13 = str(cShift13 + dShift13)
                roundKey13 = FinalPermutation(shiftKey13)

                shiftKey14 = str(cShift14 + dShift14)
                roundKey14 = FinalPermutation(shiftKey14)

                shiftKey15 = str(cShift15 + dShift15)
                roundKey15 = FinalPermutation(shiftKey15)

    return roundKey1, roundKey2, roundKey3, roundKey4, roundKey5, roundKey6, roundKey7, roundKey8, roundKey9, roundKey10, roundKey11, roundKey12, roundKey13, roundKey14, roundKey15, roundKey16


def FinalPermutation(shiftkey):
    IP2 = [40, 8, 48, 16, 56, 24, 64, 32,
           39, 7, 47, 15, 55, 23, 63, 31,
           38, 6, 46, 14, 54, 22, 62, 30,
           37, 5, 45, 13, 53, 21, 61, 29,
           36, 4, 44, 12, 52, 20, 60, 28,
           35, 3, 43, 11, 51, 19, 59, 27,
           34, 2, 42, 10, 50, 18, 58, 26,
           33, 1, 41, 9, 49, 17, 57, 25]

    iteration_counter = 0
    keyLst = list()
    for position in IP2:

        if position > 48:
            pass

        else:
            if iteration_counter < 48:
                keyLst.append(shiftkey[position - 1])
                iteration_counter += 1

    key = "".join(keyLst)
    return key


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
    for bits in copyPlaintext:
        tempPlaintext = bits.encode('utf-8')
        paddedPlainText = binascii.hexlify(tempPlaintext)
        concatPlainText += (paddedPlainText).decode("utf-8")

    # Performing PKCS5 padding
    padLen = (64 - (len(concatPlainText) % 64))
    padBlocks = int(padLen / 8)
    mod = padLen % 8

    concatPlainText += "0" * mod
    concatPlainText += ("0" + str(padBlocks)) * int((padLen - 2) / 2)

    # Converting text from hex to decimal
    binPlainText = bin(int(concatPlainText, 16))[2:]

    if len(binPlainText) % 64 != 0:
        while (len(binPlainText) % 64 != 0):
            binPlainText += "0" * (len(binPlainText) % 64)


pkcs5()

totalPlainTextBlocks = int(len(binPlainText) / 64)
for iteration in range(0, totalPlainTextBlocks):
    randomIV = os.urandom(8)
    randomIVHex = binascii.hexlify(randomIV)
    ivhexSize = len(randomIVHex)
    IV = (bin(int(randomIVHex, 16))[2:]).zfill(64)
    lstIV.append(IV)


def IP():
    IP = [58, 50, 42, 34, 26, 18, 10, 2,
          60, 52, 44, 36, 28, 20, 12, 4,
          62, 54, 46, 38, 30, 22, 14, 6,
          64, 56, 48, 40, 32, 24, 16, 8,
          57, 49, 41, 33, 25, 17, 9, 1,
          59, 51, 43, 35, 27, 19, 11, 3,
          61, 53, 45, 37, 29, 21, 13, 5,
          63, 55, 47, 39, 31, 23, 15, 7]

    tempShift = list()
    for element in lstIV:  # Iterate through each IV from the IV list: lstIV
        for position in IP:  # Bit shifting

            tempShift.append(element[position - 1])

        tempStr = "".join(tempShift)
        feedEBox.append(tempStr)
        tempShift.clear()
    # print(feedEBox)
    # print(len(feedEBox))
    return feedEBox


roundKeyGen(hashKey1)
pkcs5()
IP()

lstRoundKey = (
    [roundKey1, roundKey2, roundKey3, roundKey4, roundKey5, roundKey6, roundKey7, roundKey8, roundKey9, roundKey10,
     roundKey11, roundKey12, roundKey13, roundKey14, roundKey15, roundKey16])


def EBox():
    global lstLeftBits
    global lstxorRK
    eboxRightBits = list()
    leftBits = ""

    Ebox = [32, 1, 2, 3, 4, 5,
            4, 5, 6, 7, 8, 9,
            8, 9, 10, 11, 12, 13,
            12, 13, 14, 15, 16, 17,
            16, 17, 18, 19, 20, 21,
            20, 21, 22, 23, 24, 25,
            24, 25, 26, 27, 28, 29,
            28, 29, 30, 31, 32, 1]
    # Now divide the 64-bits input into L and R, each of 32-bits


    for tempBlock in feedEBox:
        leftBits = tempBlock[0:32]
        rightBits = tempBlock[32:64]
        for eposition in Ebox:
            eboxRightBits.append(rightBits[eposition - 1])
            stringRBits = "".join(eboxRightBits)
        for keys in lstRoundKey:
            # Now we XoR stringRBits ^ Key1
            intRBits = int(stringRBits, 2)
            keyX = int(keys, 2)
            intxorRK = intRBits ^ keyX
            xorRK = bin(intxorRK)[2:].zfill(48)
            eboxRightBits.clear()
            # print(xorRK)
            # print(len(xorRK))
        lstxorRK.append(xorRK)
        lstLeftBits.append(leftBits)


EBox()


# print(lstRoundKey)

def SBox():  # This function performs the tedious S-Box implementation

    lstLeftBits
    lstxorRK

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


# Divide the 48-bits into 8 parts of 6-bits each
    for blocks in lstxorRK:
        block1 = blocks[0:6]
        block2 = blocks[6:12]
        block3 = blocks[12:18]
        block4 = blocks[18:24]
        block5 = blocks[24:30]
        block6 = blocks[30:36]
        block7 = blocks[36:42]
        block8 = blocks[42:48]

SBox()
