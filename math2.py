__author__ = 'admin'

import itertools, math
import itertools2

def vecadd(a,b):
    """addition of vectors of inequal lengths"""
    return map(sum, itertools.izip_longest(a,b,fillvalue=0))

def vecmul(a,b):
    """product of vectors of inequal lengths"""
    return [a[i]*b[i] for i in range(min([len(a),len(b)]))]

def vecdiv(a,b):
    """quotient of vectors of inequal lengths"""
    return [a[i]/b[i] for i in range(min([len(a),len(b)]))]

def veccompare(a,b):
    """compare values in 2 lists. returns triple number of paris where [a<b, a==b, a==c]"""
    res=[0,0,0]
    for i in range(min([len(a),len(b)])):
        if a[i]<b[i]:res[0]+=1
        elif a[i]==b[i]:res[1]+=1
        else:res[2]+=1
    return res

def variance(data):
    """variance of data"""
    s = 0.0
    for value in data:
        s += value
    mean = s/len(data)
    s = 0.0
    for value in data:
        s += (value - mean)**2
    var = s/(len(data) - 1)
    return var

