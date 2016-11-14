# In this variation the key is hashed before

import math, string

binBits = ""
hexChunks = ""
lstHexBits = list()
tempChunk = ""
iteration = 0
key = ""
lstHashPrimes = list()

lst64Primes = list([0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
                    0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
                    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
                    0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
                    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
                    0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
                    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
                    0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
                    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
                    0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
                    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
                    0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
                    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
                    0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
                    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
                    0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2])




def compression(lstHex, lstHashPrimes, lst64Primes):
    global a, b, c, d, e, f, g, h
    global key
    lstDigest = list()

    for i in range(64):
        S1 = rightRotate(e, 6) ^ rightRotate(e, 11) ^ rightRotate(e, 25)
        ch = (e & f) ^ ((~e) & g)
        temp1 = h + S1 + ch + lst64Primes[i] + int(lstHex[i], 16)  # % (2**32)
        S0 = rightRotate(a, 2) ^ rightRotate(a, 13) ^ rightRotate(a, 22)
        maj = (a & b) ^ (a & c) ^ (b & c)
        temp2 = S0 + maj

        h = g
        g = f
        f = e
        e = (d + temp1) & 0xFFFFFFFF
        d = c
        c = b
        b = a
        a = (temp1 + temp2) & 0xFFFFFFFF
        # print(hex(a), "", hex(b), "", hex(c), "", hex(d), "", hex(e), "", hex(f), "", hex(g), "", hex(h))

    lstHashPrimes[0] = (lstHashPrimes[0] + a) & 0xFFFFFFFF
    lstHashPrimes[1] = (lstHashPrimes[1] + b) & 0xFFFFFFFF
    lstHashPrimes[2] = (lstHashPrimes[2] + c) & 0xFFFFFFFF
    lstHashPrimes[3] = (lstHashPrimes[3] + d) & 0xFFFFFFFF
    lstHashPrimes[4] = (lstHashPrimes[4] + e) & 0xFFFFFFFF
    lstHashPrimes[5] = (lstHashPrimes[5] + f) & 0xFFFFFFFF
    lstHashPrimes[6] = (lstHashPrimes[6] + g) & 0xFFFFFFFF
    lstHashPrimes[7] = (lstHashPrimes[7] + h) & 0xFFFFFFFF

    a, b, c, d, e, f, g, h = lstHashPrimes

    for j in lstHashPrimes:
        lstDigest.append(hex(j)[2:].zfill(8))
        # print(lstDigest)

    print("".join(lstDigest))
    print(len("".join(lstDigest)))
    key = "".join(lstDigest)
    return key


def rbitShifter(lstHex):
    global lstHashPrimes

    for i in range(16, 64):
        s0 = rightRotate(int(lstHex[i - 15], 16), 7) ^ rightRotate(int(lstHex[i - 15], 16), 18) ^ (
            int(lstHex[i - 15], 16) >> 3)
        s1 = rightRotate(int(lstHex[i - 2], 16), 17) ^ rightRotate(int(lstHex[i - 2], 16), 19) ^ (
            int(lstHex[i - 2], 16) >> 10)
        strng = (int(lstHex[i - 16], 16) + s0 + int(lstHex[i - 7], 16) + s1) & 0xFFFFFFFF
        lstHex.append(hex(strng))
        # print(lstHex)
    # lstTemp2 = lstHex
    # lstHex.clear()
    return compression(lstHex, lstHashPrimes, lst64Primes)


# Right Rotate Bits
def rightRotate(x, y):
    return ((x >> y) | (x << (32 - y))) & 0xFFFFFFFF


# str = "(45/5/(4979%\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\f7c3006e2f9faec5718b71a36430d1da26962375fffc00b386a1520c84f947a2"


def hexBits(strng):
    global lstHexBits
    lstHexBits.clear()
    # lstTemp = list()
    # hexWords = hex(int(strng,2))
    for i in range(0, int(len(strng)), 32):
        tempHex = strng[i:i + 32]
        hexWords = hex(int(tempHex, 2))
        lstHexBits.append(hexWords)
    return rbitShifter(lstHexBits)


def ascii_bin(strng, l):
    global tempChunk
    global binBits
    global iteration
    str_binary = strng.encode("ascii")

    if l >= 64:
        if int(len(strng)) == 64:
            binBits += "".join(format(x, '08b') for x in str_binary)  # 64 chars go here
            iteration -= 1
            return binBits
        elif strng == "":
            binBits += "".join(format(x, '08b') for x in str_binary)
            binBits += "1"
            addStrLen = format((l * 8), '08b').zfill(64)
            padZero = 448 - (len(binBits))
            binBits += "0" * padZero
            binBits += addStrLen
            iteration -= 1
            return binBits
        else:
            binBits += "".join(format(x, '08b') for x in str_binary)
            binBits += "1"
            addStrLen = format((l * 8), '08b').zfill(64)
            padZero = 448 - (len(binBits))
            binBits += "0" * padZero
            binBits += addStrLen
            iteration -= 1
            return binBits

    if l >= 56:
        if strng == "":  # s lenght is between 56 and 63 (inclusive)
            binBits += "".join(format(x, '08b') for x in str_binary)
            addStrLen = format((l * 8), '08b').zfill(64)
            padZero = 448 - (len(binBits))
            binBits += "0" * padZero
            binBits += addStrLen
            iteration -= 1
            return binBits

        else:  # When input string length is > 0
            binBits += "".join(format(x, '08b') for x in str_binary)  # 56 chars go here
            padZero = 448 - len(binBits)
            if padZero == 0 or padZero < 0:  # This will be true only when there are 56 chars and not add length
                binBits += "1"
                padZero = 512 - (len(binBits))
                binBits += "0" * padZero
                iteration -= 1
                return binBits

    else:
        binBits += "".join(format(x, '08b') for x in str_binary)
        addStrLen = format((l * 8), '08b').zfill(64)
        binBits += "1"
        padZero = 448 - len(binBits)
        binBits += "0" * padZero
        binBits += addStrLen
        iteration -= 1
        return binBits

    return binBits


def bitChunks32(s):
    global binBits
    global tempChunk
    global iteration
    global lstHashPrimes
    global key
    global a, b, c, d, e, f, g, h
    print("S", "\n", s, "\n", len(s))
    lstHashPrimes = list([0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
                          0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19])
    a, b, c, d, e, f, g, h = lstHashPrimes
    # s0 = s.decode('utf-8')  # remove this comment tag afterwards
    # print("S", "\n", s0, "\n", len(s0))
    # global a, b, c, d, e, f, g, h

    block = 0
    iteration = math.ceil(int(len(s) * 8) / 447)
    chunkBits = ""

    lstBinBits = list()
    lenString = len(s)
    tempChunk = ""
    for i in range(0, int(len(s)), 64):
        chunk = s[i:i + 64]
        tempChunk += chunk
        chunkBits = ascii_bin(chunk, lenString)

        if len(
                s) < 56:  # int(len(tempChunk)) == int(len(s)) and iteration == 0 and block == 0: # This will only work for input strings with char length <= 55
            lstBinBits.append(chunkBits)
            block += 1
            strhashWords = hexBits(chunkBits)

        if len(chunkBits) == 512 and int(len(tempChunk)) != int(len(s)):
            lstBinBits.append(chunkBits)
            block += 1
            strhashWords = hexBits(chunkBits)
            chunkBits = ""
            binBits = ""
            lstBinBits.clear()

        if int(len(tempChunk)) == int(len(s)) and (iteration == 0 or iteration == 1) and int(
                        len(s) > 55):  # This will only work for input strings with char length > 55
            lstBinBits.append(chunkBits)
            block += 1
            strhashWords = hexBits(chunkBits)
            chunkBits = ""
            binBits = ""
            if (iteration == 0 or iteration == 1) and int(len(chunk)) > 55:  # When the last block was of 56 chars
                chunkBits = ascii_bin(chunkBits, lenString)
                strhashWords = hexBits(chunkBits)
            else:  # When the length of block was below 56 chars
                pass

    return key


# bitChunks32(str)


def HMAC(k, m):
    global key
    lstopad = list()
    blocksize = 64
    k0 = bytes(k.encode('utf-8'))
    print (k0)
    k0 = k0 + bytes(blocksize - len(k0))
    print(k0,len(k0))
    mbits = m.encode('utf-8')

    # print(k0, '\n', len(k0), '\n', type(k0))
    trans_5C = bytes((x ^ 0x5C) for x in range(256))
    trans_36 = bytes((x ^ 0x36) for x in range(256))

    opad = (k0.translate(trans_5C))
    print("OPAD ",opad,"\n","Lenght of OPAD = ",len(opad))
    print("OPAD ", str(opad), "\n", "Lenght of OPAD = ", len(opad))
    ipad = (k0.translate(trans_36))
    print("IPAD AND LENGTH ",ipad, len(ipad))


    # print(len(ipad), len(opad))

    # print("MBITS ", mbits, len(mbits))

    # print("ipad", type(ipad), "Msg ", type(mbits))
    appendIpad = ipad + mbits
    print(type(ipad), type(mbits), type(k0),type(appendIpad))
    # print("APPEND IPAD ", appendIpad, "\n", len(appendIpad))

    appendIpad = appendIpad.decode('utf-8')
    # print("APPEND IPAD ", appendIpad, "\n", len(appendIpad))
    print(type(ipad), type(mbits), type(k0), type(appendIpad))

    digest = bitChunks32(appendIpad)
    # print ("Opad",type(opad),"digest ",type(digest))

    # d1 = bytearray(digest.encode('utf-8'))
    d1 = bytes(digest.encode('utf-8'))
    print("Opad", type(opad), "d1 ", type(d1),len(d1))

    # opad_c = str(opad,'utf-8')

    # print("STROPAD ",opad_c,"\n",len(opad_c))
    # # print("Opad_c", type(opad_c), "d1 ", type(digest))
    # print("Opad_c", opad_c)

    KxorOpad = opad + d1
    # KxorOpad2 = KxorOpad.decode()
    print ("KxorOpad","\n",KxorOpad,"\n",len(KxorOpad))
    print("KxorOpad", type(KxorOpad), "digest ", type(d1))

    KxorOpad = KxorOpad.decode('utf-8')
    print ("KxorOpad","\n",KxorOpad,"\n",len(KxorOpad),type(KxorOpad))

    digest2 = bitChunks32(KxorOpad)
    # print ("Digest2 = ",digest2)


HMAC("thisisthekey", "kanishk sharan really wants to crack this")
