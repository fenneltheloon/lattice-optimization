import scipy.integrate
import csv
import math
import numpy

BIN_NUMBER = 12
SPACE_GROUPS = 100

def chi(x):
    out = scipy.integrate.quad(lambda t: math.exp(-((t ** 2)/2)), 0, x) 
    return out[0]

output_file = open("bin_data.csv", "w")
fwriter = csv.writer(output_file)
row_1 = ["z-value", "Bin 1", "Bin 2", "Bin 3", "Bin 4", "Bin 5",\
         "Bin 6", "Bin 7", "Bin 8", "Bin 9", "Bin 10", "Bin 11",\
         "Bin 12"]
fwriter.writerow(row_1)

for z in numpy.linspace(0, 6, 12, endpoint=False):
    Bins = [z]
    if z == 0:
        for i in range(1, BIN_NUMBER + 1):
            Bins.append((SPACE_GROUPS * i) / BIN_NUMBER)
    else:
        for i in range(1, BIN_NUMBER + 1):
            Bins.append(SPACE_GROUPS * ((chi((z * i) / BIN_NUMBER)) / (chi(z))))
    
    fwriter.writerow(Bins)