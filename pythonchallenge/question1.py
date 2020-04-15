

someStr = "g fmnc wms bgblr rpylqjyrc gr zw fylb. rfyrq ufyr amknsrcpq ypc dmp. bmgle gr gl zw fylb gq glcddgagclr ylb rfyr'q ufw rfgq rcvr gq qm jmle. sqgle qrpgle.kyicrpylq() gq pcamkkclbcb. lmu ynnjw ml rfc spj."

someStr = "http://www.pythonchallenge.com/pc/def/map.html"

alphabet = "abcdefghijklmnopqrstuvwxyz"
# decodedStr = ""

# for i in range(len(someStr)):
#     index = alphabet.find(someStr[i])
#     if(index != -1):
#         j = index + 2
#         if(len(alphabet) - 1 < j):
#             j -= len(alphabet)
#         decodedStr = decodedStr + alphabet[j]
#     else:
#         decodedStr = decodedStr + someStr[i]

# print(decodedStr)


encodeAlphabet = "cdefghijklmnopqrstuvwxyzab"

# code = {"a": "c", "b": "d", "c": "e", "d": "f", 
#         "e": "g", "f": "h", "g": "i", "h": "j", 
#         "i": "k", "j": "l", "k": "m", "l": "n", 
#         "m": "o", "n": "p", "o": "q", "p": "r", 
#         "q": "s", "r": "t", "s": "u", "t": "v", 
#         "u": "w", "v": "x", "w": "y", "x": "z",
#         "y": "a", "z": "b"}

trans = str.maketrans(alphabet, encodeAlphabet)
print(trans)
print(someStr.translate(trans))

