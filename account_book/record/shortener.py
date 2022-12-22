
import random

words = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
         'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
         'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
         'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f',
         'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
         'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
         'w', 'x', 'y', 'z', '0', '1', '2', '3',
         '4', '5', '6', '7', '8', '9',]


def encode(index):
    result = "".join(random.sample(words, 6))
    return result


def decode(string):
    base = 62
    strlen = len(string)
    num = 0

    idx = 0
    for char in string:
        power = (strlen - (idx+1))
        num += words.index(char) * (base**power)
        idx += 1

    return num
