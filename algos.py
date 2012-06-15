import exceptions

def num (s):
    try:
        return int(s)
    except exceptions.ValueError:
        return float(s)
    
def reverse(s):
    """Reverse string"""
    result=''
    length = len(s)
    for x in range(0,length):
        result+=s[length-1-x]
    return result

def str_base(num, base, numerals = '0123456789abcdefghijklmnopqrstuvwxyz'):
    if base < 2 or base > len(numerals):
        raise ValueError("str_base: base must be between 2 and %i" % len(numerals))

    if num == 0:
        return '0'

    if num < 0:
        sign = '-'
        num = -num
    else:
        sign = ''

    result = ''
    while num:
        result = numerals[num % (base)] + result
        num //= base

    return sign + result

def is_palindrome(num, base=10):
    """Check if 'num' in base 'base' is a palindrome, that's it, if it can be
    read from left to right and right to left being the same number"""
    s = str_base(num,base)
    return s==reverse(s)

def int2word(n):
    """convert an integer number n into a string of english words"""
    # from http://www.daniweb.com/code/snippet609.html

    ones = ["", "one ","two ","three ","four ", "five ",
            "six ","seven ","eight ","nine "]

    tens = ["ten ","eleven ","twelve ","thirteen ", "fourteen ",
            "fifteen ","sixteen ","seventeen ","eighteen ","nineteen "]

    twenties = ["","","twenty ","thirty ","forty ",
                "fifty ","sixty ","seventy ","eighty ","ninety "]

    thousands = ["","thousand ","million ", "billion ", "trillion ",
                 "quadrillion ", "quintillion ", "sextillion ", "septillion ","octillion ",
                 "nonillion ", "decillion ", "undecillion ", "duodecillion ", "tredecillion ",
                 "quattuordecillion ", "sexdecillion ", "septendecillion ", "octodecillion ",
                 "novemdecillion ", "vigintillion "]
    # break the number into groups of 3 digits using slicing
    # each group representing hundred, thousand, million, billion, ...
    n3 = []
    # create numeric string
    ns = str(n)
    for k in range(3, 33, 3):
        r = ns[-k:]
        q = len(ns) - k
        # break if end of ns has been reached
        if q < -2:
            break
        else:
            if  q >= 0:
                n3.append(int(r[:3]))
            elif q >= -1:
                n3.append(int(r[:2]))
            elif q >= -2:
                n3.append(int(r[:1]))

    #print n3  # test

    # break each group of 3 digits into ones, tens/twenties, hundreds and form a string
    nw = ""
    for i, x in enumerate(n3):
        b1 = x % 10
        b2 = (x % 100)//10
        b3 = (x % 1000)//100
        #print b1, b2, b3  # test
        if x == 0:
            continue  # skip
        else:
            t = thousands[i]
        if b2 == 0:
            nw = ones[b1] + t + nw
        elif b2 == 1:
            nw = tens[b1] + t + nw
        elif b2 > 1:
            nw = twenties[b2] + ones[b1] + t + nw
        if b3 > 0:
            if nw=="":
                nw = ones[b3] + "hundred"
            else:
                nw = ones[b3] + "hundred and " + nw
    return nw

