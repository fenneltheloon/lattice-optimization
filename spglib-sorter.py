#!./env python
# spglib-parser.py
# Ethan Meltzer
# 2023-06-15

# Reads in VASP POSCAR files from a user-specified directory, determines their
# space group, and then places them into a subfolder labeled with that space
# group.

import sys
import os
import re
import spglib

NUM_AG = 9
NUM_BI = 9
NUM_CU = 18
INDEX_FNAME = "INDEX.vasp"

# Will match exactly the config specifier on the first line of the POSCAR file
FLINE_RE = r"Ag(?:-\d{1,2}){9}_Bi(?:-\d{1,2}){9}_Cu(?:-\d{1,2}){18}"
# Will match all indices in the configuration line in order of appearance
INDICES_RE = r"(\d{1,2})"

# First check for args and do some error handling
n = len(sys.argv)

if len(sys.argv) < 2:
    print("Please give directory path as an argument.")
    sys.exit(1)

if not os.path.isdir(sys.argv[1]):
    print("Make suere that path to directory is specified correctly.")
    sys.exit(1)
else:
    print("Opening " + sys.argv[1] + " ...")

# Read the fully populated POSCAR and generate the dictionary of indicies
try:
    f = open(os.path.join(sys.argv[1], INDEX_FNAME), "r")
except OSError:
    print(f"Make sure that {INDEX_FNAME} is in the root of {sys.argv[1]}.")
    sys.exit(1)
else:
    print(f"Found {INDEX_FNAME}...")

flines = f.readlines()

# Get lattice constant
try:
    lattice_constant = float(flines[1])
except ValueError:
    print("Could not find lattice constant on line 2")
    sys.exit(1)
else:
    print(f"Lattice constant: {lattice_constant}")

# Get the lattice vectors
try:
    A = [float(x) for x in flines[2].split()]
    B = [float(x) for x in flines[3].split()]
    C = [float(x) for x in flines[4].split()]
except ValueError:
    print("Could not parse lattice vectors on lines 3, 4, 5.")
    sys.exit(1)
else:
    print(f"a = {A}")
    print(f"b = {B}")
    print(f"c = {C}")

# Read in the # of each element and in the correct order
Elements = zip(flines[5].split(), flines[6].split())
assert len(Elements) == 3
# Make sure we are reading in Direct mapping
assert flines[7].strip() == "Direct"

line_offset = 8
AgBiAll = []
CuAll = []
IAll = []

# Load up the lists that index the possible positions for each element and
# check to make sure that each element has correct # of spots
for element in Elements:
    match element[0]:
        case "Ag" | "Bi":
            assert element[1] == 27
            for i in range(element[1]):
                AgBiAll.append([
                    float(x) for x in flines[line_offset + i].split()
                ])
            print(f"Found {element[1]} positions for {element[0]}.")
            line_offset += element[1]
        case "Cu":
            assert element[1] == 108
            for i in range(element[1]):
                CuAll.append([
                    float(x) for x in flines[line_offset + i].split()
                ])
            print(f"Found {element[1]} positions for {element[0]}.")
            line_offset += element[1]
        case "I":
            assert element[1] == 54
            for i in range(element[1]):
                IAll.append(flines[line_offset + i].split())
                IAll[i] = [float(x) for x in IAll[i]]
            print(f"Found {element[1]} positions for {element[0]}.")
            line_offset += element[1]
        case _:
            print("Syntax error on lines 6 and 7")
            sys.exit(1)

# Create the lattice variable that will be used by spglib
lattice = [[x * lattice_constant for x in A],
           [x * lattice_constant for x in B],
           [x * lattice_constant for x in C]]

# The spglib numbers variable will also be a constant which we can define here:
numbers = [1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3,
           3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]

# Walk the filepath and check for any files named POSCAR
for dirpath, dirnames, filenames in os.walk(sys.argv[1]):
    # If the current directory is a number, skip the directory.
    # Exclusively numbered subdirectories are where the output is going,
    # and this would cause the program to run forever.
    if dirpath.split("/")[-1].isnumeric():
        continue

    for file in filenames:
        f = open(os.path.join(dirpath, file), "r")
        flines = f.readlines()

        # If the first line of the file does not contain a specified
        # configuration, skip.
        if re.match(FLINE_RE, flines[0]) is None:
            f.close()
            continue

        Indices = re.findall(INDICES_RE, flines[0])
        # Indices should be len 36 because we made it past the first regex
        assert len(Indices) == 36

        Ag = [int(x) for x in Indices[0:9]]
        Bi = [int(x) for x in Indices[9:18]]
        Cu = [int(x) for x in Indices[18:36]]

        # Create and initialize the positions variable for spglib
        positions = []

        # TODO: fill in the positions variable with the indexed vectors
