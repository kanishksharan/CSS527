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

    return roundKey1,roundKey2,roundKey3,roundKey4,roundKey5,roundKey6,roundKey7,roundKey8,roundKey9,roundKey10,roundKey11,roundKey12,roundKey13,roundKey14,roundKey15,roundKey16

def FinalPermutation (shiftkey):

    IP2 = [40     ,8   ,48    ,16    ,56   ,24    ,64   ,32,
            39     ,7   ,47    ,15    ,55   ,23    ,63   ,31,
            38     ,6   ,46    ,14    ,54   ,22    ,62   ,30,
            37     ,5   ,45    ,13    ,53   ,21    ,61   ,29,
            36     ,4   ,44    ,12    ,52   ,20    ,60   ,28,
            35     ,3   ,43    ,11    ,51   ,19    ,59   ,27,
            34     ,2   ,42    ,10    ,50   ,18    ,58   ,26,
            33     ,1   ,41     ,9    ,49   ,17    ,57   ,25]

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

    filePlainText = open ("inputFile.txt","r")
    copyPlaintext = ("\n".join(filePlainText.readlines()))
    filePlainText.close()

    # Converting plaintext to Hexademical
    for bits in copyPlaintext:
            tempPlaintext = bits.encode ('utf-8')
            paddedPlainText = binascii.hexlify(tempPlaintext)
            concatPlainText += (paddedPlainText).decode("utf-8")


    # Performing PKCS5 padding
    padLen = (64 - (len(concatPlainText) % 64))
    padBlocks = int(padLen/8)
    mod = padLen%8

    concatPlainText += "0" * mod
    concatPlainText += ("0"+str(padBlocks)) * int((padLen-2)/2)

    # Converting text from hex to decimal
    binPlainText = bin(int(concatPlainText, 16))[2:]

    while (len(binPlainText)%64 != 0):
            binPlainText += "0" * (len(binPlainText)%64)
    

roundKeyGen(hashKey1)
pkcs5()
