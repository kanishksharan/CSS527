import os
import binascii

# Declaring global variables
binBits = ""
hexChunks = ""
lstHexBits = list()

lstHashPrimes = list([1779033703,3144134277,1013904242,2773480762,1359893119,2600822924,528734635,1541459225])

lst64Primes = list ([1116352408,1899447441,3049323471,3921009573,961987163,1508970993,2453635748,2870763221,
3624381080,310598401,607225278,1426881987,1925078388,2162078206,2614888103,3248222580,3835390401,4022224774,
264347078,604807628,770255983,1249150122,1555081692,1996064986,2554220882,2821834349,2952996808,3210313671,
3336571891,3584528711,113926993,338241895,666307205,773529912,1294757372,1396182291,1695183700,1986661051,
2177026350,2456956037,2730485921,2820302411,3259730800,3345764771,3516065817,3600352804,4094571909,275423344,
430227734,506948616,659060556,883997877,958139571,1322822218,1537002063,1747873779,1955562222,2024104815,2227730452,
2361852424,2428436474,2756734187,3204031479,3329325298])

a,b,c,d,e,f,g,h = lstHashPrimes


# Convert ASCII to Binary
def ascii_bin(strng, l):
    str_binary = strng.encode("ascii")
    addStrLen = format(int(l * 8), '08b').zfill(64)
    global binBits
    if int(len(strng)) % 4 != 0:
        binBits += "".join(format(x, '08b') for x in str_binary)
        binBits += "10000000"
        padZero = 448 - len(binBits)
        binBits += "0" * padZero
        binBits += addStrLen
        return binBits

    else:
        binBits += "".join(format(x, '08b') for x in str_binary)
        # print (binBits)
        return binBits


str = "ksharan"

# This function gives the 16 Words in Hexadecimal
def hexBits(strng):
    global lstHexBits
    hexWords = hex(int(strng,2))[2:]
    for i in range(0, int(len(hexWords)), 8):
        tempHex = hexWords[i:i + 8]
        lstHexBits.append(tempHex)

    return lstHexBits

# Divide input text in 32-bits chunks
def bitChunks32(s):
    global binBits
    chunkBits = ""
    block = 0
    lstBinBits = list()
    lstHashWords = list()
    lenString = len(s)
    for i in range(0, int(len(s)), 4):
        chunk = str[i:i + 4]
        chunkBits = ascii_bin(chunk, lenString)
        if len(chunkBits) == 512:
            lstBinBits.append(chunkBits)
            block += 1

    strhashWords = hexBits(chunkBits)
    return chunkBits

bitChunks32(str)


# Unit test this part
def rbitShifter(lstHexBits):

    for i in range (16,64):
        s0 = bin((int(lstHexBits[i-15],16)>> 7) ^ (int(lstHexBits[i-15],16)>> 18) ^ (int(lstHexBits[i-15],16)>> 3))
        tmp0 = int(s0,2)
        s1 = bin((int(lstHexBits[i-2],16)>> 17) ^ (int(lstHexBits[i-2],16)>> 19) ^ (int(lstHexBits[i-2],16)>> 10))
        tmp1 = int(s1,2)
        strng = hex(int(lstHexBits[i-16],16) + tmp0 + int(lstHexBits[i-7],16) + tmp1)[2:]
        lstHexBits.append(strng)
    return lstHexBits

def compression(lstHexBits,lst64Primes):
    global lstHashPrimes
    lstDigest = list()
    for i in range(64):
        S0 = (lstHashPrimes[0]>> 2) ^ (lstHashPrimes[0]>> 13) ^ (lstHashPrimes[0]>> 22)
        S1 = (lstHashPrimes[4]>> 6) ^ (lstHashPrimes[4]>> 11) ^ (lstHashPrimes[4]>> 25)
        maj = (lstHashPrimes[0] & lstHashPrimes[1]) ^ (lstHashPrimes[0] & lstHashPrimes[2]) ^ (lstHashPrimes[1] & lstHashPrimes[2])
        ch = (lstHashPrimes[4] & lstHashPrimes[5]) ^ (~int(lstHashPrimes[4]) & lstHashPrimes[6])
        temp1 = lstHashPrimes[7] + S1 + ch + lst64Primes[i] + int(lstHexBits[i],16)
        temp2 = S0 + maj

        lstHashPrimes[7] = lstHashPrimes[6]
        lstHashPrimes[6] = lstHashPrimes[5]
        lstHashPrimes[5] = lstHashPrimes[4]
        lstHashPrimes[4] = lstHashPrimes[3] + temp1
        lstHashPrimes[3] = lstHashPrimes[2]
        lstHashPrimes[2] = lstHashPrimes[1]
        lstHashPrimes[1] = lstHashPrimes[0]
        lstHashPrimes[0] = temp1 + temp2
    for j in lstHashPrimes:
        lstDigest.append(hex(j)[2:])

    print ("".join(lstDigest))
    print (len("".join(lstDigest)))
    return "".join(lstDigest)

rbitShifter(lstHexBits)
compression(lstHexBits,lst64Primes)

# print (lstHexBits)
# print (len(lstHexBits))
