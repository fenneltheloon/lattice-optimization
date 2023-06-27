#!./env python
# first-gen-filler.py
# Ethan Meltzer
# 2023-06-19
# Python 3.11.4
###############################################################################
# Takes an INDEX.vasp file in as an argument containing all possible sites for
# each atom, randomly generates possible configurations, and sorts them into
# subdirectory bins according to their space group, determined by spglib.
###############################################################################
# Arguments:
# -h --help:  Prints a help message
# -i --index: "path/to/INDEX.vasp" points to the index file containing all
#             possible combinations
# -b --bins:  Specifies the number of bins that will be sorted into by spglib,
#             maximum 230, minimum 1. Bins will be of equal size, but different
#             amounts of space groups will be allocated to each bin on an
#             exponential curve
# -n --number: Specifies how many configurations there will be in the
# generation

import argparse
import sys
import os
import random
import scipy
import math
import pymatgen

def phi(x):
    return (1 / math.sqrt(2 * math.pi)) * (scipy.integrate.quad(lambda t:\
            math.exp(-((t ** 2) / 2)), 0, x))

CU_OCC = 18
CU_AV = 108
AG_OCC = 9
BI_OCC = 9
AG_BI_AV = 27
I_AV_OCC = 54
SPACE_GROUPS = 230

arg_parser = argparse.ArgumentParser()

arg_parser.add_argument("-i", "--index", type=argparse.FileType("r"),
                        required=True, help="provide \"path/to/INDEX.vasp\",\
                        the index file containing all atomic positions")
arg_parser.add_argument("-b", "--bins", type=int, default=1, help="Specifies\
                        the number of bins that will be sorted into by spglib\
                        max 230, min (default) 1. Bins will be of equal size,\
                        but different amounts of space groups will be\
                        allocated to each bin on an exponential curve.")
arg_parser.add_argument("-n", "--number", type=int, default=100,
                        help="Specifies how many configurations there will be\
                        in the generation. Default 100.")
arg_parser.add_argument("-a", "--aggressiveness", type=float, default=3, help=\
                        "Specifies how aggressively biased the binning will be\
                        towards higher order space groups. Mathematically, this\
                        is specifying a z-score as a cutoff on the curve\
                        that is being sampled. Default 3.")

args = arg_parser.parse_args()

# Check args for validity
if (args.bins not in range(1, 231)) or (args.number <= 0) or\
        (args.number < args.bins):
    print("Make sure arguments are within bounds and that -n >= -b.")
    sys.exit(1)

# Read in INDEX.vasp into linetable and parse components
index = args.index.readlines()

lattice_constant = index[1]
# A: 0, B: 1, C: 2
LatticeMatrix = [index[i] for i in range(2, 5)]

Elements = zip(index[5].split(), [int(x) for x in index[6].split()])
# Just making sure that the file is in the correct format :)
assert len(Elements) == 3
assert index[7].strip() == "Direct"

line_offset = 8
AgBiIndex = []
CuIndex = []
IIndex = []

# Load up the lists that index the possible positions for each element and
# check to make sure that each element has the correct number of spots
for element in Elements:
    match element[0]:
        case "Ag" | "Bi":
            assert element[1] == AG_BI_AV
            for i in range(element[1]):
                AgBiIndex.append(index[line_offset + i])
            print(f"Found {element[1]} positions for {element[0]}.")
            line_offset += element[1]
        case "Cu":
            assert element[1] == CU_AV
            for i in range(element[1]):
                CuIndex.append(index[line_offset + i])
            print(f"Found {element[1]} positions for {element[0]}.")
            line_offset += element[1]
        case "I":
            assert element[1] == I_AV_OCC
            for i in range(element[1]):
                IIndex.append(index[line_offset + i])
            print(f"Found {element[1]} positions for {element[0]}.")
            line_offset += element[1]
        case _:
            print("Syntax error on lines 6 and 7.")

# Calculate the distribution of space groups into bins on a normal
# distribution
Bins = [math.round(2 * SPACE_GROUPS *\
                    phi((args.aggressiveness * i) / args.bins)) for i in\
                    range(1, args.bins)]
Bins[args.bins - 1] = SPACE_GROUPS

# Create subdirectories for each bin
parent_dir = os.path.dirname(args.index)
for i in range(0, args.bins):
    os.mkdir(os.path.join(parent_dir, str(i)))

# Now generate the random config
for i in range(args.number):
    AgBiOcc = random.choices(AgBiIndex, k=AG_OCC + BI_OCC)
    AgOcc = AgBiOcc[0:AG_OCC]
    BiOcc = AgBiOcc[AG_OCC:AG_OCC + BI_OCC]
    CuOcc = random.choices(CuIndex, k=CU_OCC)

    # Create the new file and write its contents
    vasp_file = open(f"{i}.vasp", "w")
    vasp_file.write(f"{i}\n")
    vasp_file.write(lattice_constant)
    vasp_file.writelines(LatticeMatrix)
    vasp_file.write(f"{'Ag':<3}{'Bi':<3}{'Cu':<3}{'I':<3}\n")
    vasp_file.write(f"{AG_OCC:3d}{BI_OCC:3d}{CU_OCC:3d}{I_AV_OCC:3d}\n")
    vasp_file.writelines(AgOcc)
    vasp_file.writelines(BiOcc)
    vasp_file.writelines(CuOcc)
    vasp_file.writelines(IIndex)

    # Calculate and append spacegroup to the start of the file
    poscar = pymatgen.io.vasp.inputs.Poscar\
        .from_file(f"{i}.vasp", check_for_POTCAR=False, read_velocities=False)

    spacegroup = pymatgen.symmetry.analyzer.SpacegroupAnalyzer(poscar)\
        .get_space_group_number()

    vasp_file.seek(0)
    vfline = vasp_file.readline()
    vfline = vfline + f" ({spacegroup})"
    vasp_file.seek(0)
    vasp_file.writeline(vfline)
    vasp_file.close()

    # Now determine the proper bin and move file into that bin.
    for j in range(0, args.bins):
        if spacegroup <= Bins[j]:
            new_path = os.path.join(parent_dir, j, f"{i}.vasp")
            os.rename(f"{i}.vasp", new_path)
            break
