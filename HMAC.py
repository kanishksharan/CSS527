# Convert ASCII to Binary
def ascii_bin(strng):
    str_binary = strng.encode("ascii")
    addStrLen = format(int(len(strng)),'08b').zfill(64)
    if int(len(strng)) % 4 != 0:
        binBits = "".join(format(x, '08b') for x in str_binary)
        binBits += "10000000"
        padZero = 448-len(binBits)
        binBits += "0"*padZero
        binBits += addStrLen
        return binBits

    else:
        binBits = "".join(format(x, '08b') for x in str_binary)
        return binBits


str = "sh"


# Divide input text in 32-bits chunks
def bitChunks32(s):
    loopCounter = 0

    for i in range(0, int(len(str)), 4):
        chunk = str[i:i + 4]
        BinBits = ascii_bin(chunk)
        print(BinBits)
        loopCounter += 1

        return BinBits


bitChunks32(str)
