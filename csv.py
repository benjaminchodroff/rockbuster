import os
import sys
from operator import itemgetter

f = open("diamonds.txt","r")
lines = f.readlines()

dtype = ["BR","PR","EM","OV","MQ","PS","AS","CU","RA","HS"]
def shape(x):
    return {
        'BR' : 1,
        'PR' : 2,
        'EM' : 3,
        'OV' : 4,
        'MQ' : 5,
        'PS' : 6,
        'AS' : 7,
        'CU' : 8,
        'RA' : 9,
        'HS' : 10
    }[x]

def color(x):
    return {
        'D' : 1,
        'E' : 2,
        'F' : 3,
        'G' : 4,
        'H' : 5,
        'I' : 6,
        'J' : 7,
        'K' : 8,
        'FC' : 100,
        'FIY' : 100
    }[x]

def clarity(x):
    return {
        'F' : 1,
        'FL' : 1,
        'IF' : 2,
        'VVS1' : 3,
        'VVS2' : 4,
        'VS1+' : 5,
        'VS1' : 5,
        'VS2+' : 6,
        'VS2' : 6,
        'SI1' : 7,
        'SI1+' : 7,
        'SI2' : 8,
        'SI2+' : 8,
        'SI3' : 9,
        'I1' : 10,
        'I2' : 11,
        'I3' : 12,
    }[x]

def quality(x):
    return {
        'X' : 1,
        'ID' : 1,
        'VG' : 2,
        'G' : 3,
        'F' : 4,
        'P' : 5,
        'N' : 6,
    }[x]

for i in range(0,len(lines)):
    lines[i] = eval(lines[i])
    lines[i]['shape'] = shape(lines[i]['shape'])
    lines[i]['vendor_id'] = int(lines[i]['vendor_id'])
    lines[i]['price'] = int(lines[i]['price'])
    lines[i]['color'] = color(lines[i]['color'])
    lines[i]['clarity'] = clarity(lines[i]['clarity'])
    lines[i]['sym'] = quality(lines[i]['sym'])
    lines[i]['pol'] = quality(lines[i]['pol'])

lines = sorted(lines, key=itemgetter('price'))

#print "carat,color,clarity,depth,table,sym,pol,price"
for i in range(0,len(lines)):
    if lines[i]['color']>8:
        continue
    print (
        str(lines[i]['shape']) + "," +
        str(lines[i]['vendor_id']) + "," +
        str(lines[i]['carat']) + "," +
        str(lines[i]['color']) + "," +
        str(lines[i]['clarity']) + ","+  
        str(lines[i]['depth']) + "," +
        str(lines[i]['table'])+"," +
        str(lines[i]['sym'])+"," +
        str(lines[i]['pol'])+"," +
        str(lines[i]['price'])
        )

