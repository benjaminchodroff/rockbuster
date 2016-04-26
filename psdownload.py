import os
import urllib
import pdb
import sys
import math
import threading
import collections

min = float(sys.argv[1])
max = float(sys.argv[2])

def drange(start, stop, step):
    r = start
    while r < stop:
        yield r
        r += step

step = {}
pages = collections.defaultdict(dict)
diamonds = {}
foundtotal = 0

dtype = ["BR","PR","EM","OV","MQ","PS","AS","CU","RA","HS"]
# Step 0.005 to make sure we get less than 20 pages of results
step = 0.005

print "Finding all diamonds carat sized " + str(min) + " to " + str(max)
max = max - step

for t in dtype:
    inc = -1
    print "Finding diamonds of shape " + t 
    gen = drange(min,max+step*0.01,step*2)

    for j in gen:
        inc+=1
    
        totalq = 500
        print "Downloading diamonds carat sized " + str(j) + " to " + str(j+step)
        #download 20 pages (max) of results
        for i in range(1,21):
            if (25*(i-1) > totalq):
                print "   Skipping page " + str(i) + "/20"
                continue
            print "   Downloading page " + str(i) + "/20"
            pages[t][i+inc] = urllib.urlopen((
                "http://www.pricescope.com/results/ajax/?" 
                "vendor__latitude__gte=-180&type_color=1&vendor__region__contains=&clarity__lte=27&vendor__longitude__gte=-180" 
                "&shape=" + t + "&price__lte=999999&city=Richmond&hca_index__lte=10&search_key=sk_session_3068" 
                "&size__lte=" + str(j+step) +
                "&l_country=us&price__gte=100&vln_l_ct=180&latitude=37.5522003174" 
                "&size__gte=" + str(j) +
                "&vlt_g_ct=-180&clarity__gte=1&color_m=G-&l_region=VA&search=&lab=GIA&lab=AGS&type_search=1"
                "&vendor__latitude__lte=180"
                "&color_p=H%2B" 
                "&color__lte=I" 
                "&vendor__country__contains=&f=3&hca_index__gte=0&region=VA&vendor__longitude__lte=180&longitude=-77.4581985474"
                "&country=us&vln_g_ct=-180"
                "&color__gte=D"
                "&vlt_l_ct=180&sort=size"
                "&page="+str(i)
                )).readlines()
            found = 0
            for line in pages[t][i+inc]:
                if line.find("diamond-data") > 0:
                    found = 1
                elif found == 1:
                    found = 0
                    diamonds[len(diamonds)] = line.strip()
                elif line.find("We have ") > 0:
                    wehave = line.split("have ")[1].split("<b>")[0].strip()
                    totalq = int(wehave)
        foundtotal += totalq

print "Found a total of " + str(len(diamonds)) + " diamonds out of " + str(foundtotal) + " diamonds reported"
print "       "

f = open('diamonds.txt', 'w')
for i in diamonds:
    f.write(str(diamonds[i])+"\n")
f.close()


#print "Entering interactive debugger"
#pdb.set_trace()

