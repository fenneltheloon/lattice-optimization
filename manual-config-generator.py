import yaml
import pymatgen
import argparse
import sys
import sympy
import random
import itertools


def listIsAllIdentical(list):
    element = list[0]
    check = True

    for item in list:
        if item != element:
            check = False
            break

    return check


# Needs to be a list of 3d-points of type sympy.Matrix (3d colun vector)
def remove_whole_number_constants(list):
    for point in list:
        for coord in point:
            const = sum([term for term in coord.as_ordered_terms() if
                        term.is_constant()])
            if const > 0:
                const = -sympy.floor(const)
            else:
                const = -sympy.ceiling(const)
            coord = coord + const
        point.simplify()


# Given an origin (seed) and a list of symmetry operations, returns the list
# of Direct-mapped coords that generate from that origin.
def growSeed(origin, symops):
    # TODO
    incomplete()


CU_OCC = 18
CU_AV = 108
AG_OCC = 9
BI_OCC = 9
AG_BI_AV = 27
I_AV_OCC = 54
x, y, z = sympy.symbols('x, y, z')
POSSIBLE_AG_BI_SG = [i for i in range(143, 162)]
POSSIBLE_CU_SG = [143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154,
                  155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166,
                  167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178,
                  179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190,
                  195, 198]
ATTEMPT_CREATION_TIMEOUT = 100

parser = argparse.ArgumentParser(
        prog="Config Generator",
        description="Given user-inputted parameters, generates VASP POSCAR\
                files for Cu2AgBiI6 in a 3x3 crystal of a given space group\
                from 143-161."
        )

parser.add_argument("-i", "--index", help="Filepath to the index file\
        containing all possible positions for each of the elemental\
        sublattices", required=True)

# Check if positive later
parser.add_argument("-n", "--number", type=int, help="Number of configurations\
        that will be generated by the script of the specified spacegroup.",
                    required=True)

parser.add_argument("-s", "--spacegroup", type=int, choices=range(143, 162),
                    help="The spacegroup that we will be generating\
                            configurations to fall into", required=True)

parser.add_argument("-y", "--symmetries", help="Filepath to the YAML file\
        containing the symmetry operations for each of the spacegroups that\
        in the specified range.", required=True)

args = parser.parse_args()

if args.number <= 0:
    print("Please input a positiv number of configurations to generate.")
    sys.exit(1)

# Open index file
index_file = open(args.index, "r")

# Read in INDEX.vasp into linetable and parse components
index = index_file.readlines()

index_file.close()

lattice_constant = index[1]
# A: 0, B: 1, C: 2
LatticeMatrix = [index[i] for i in range(2, 5)]

Elements = [i for i in zip(index[5].split(), [int(x) for x in index[6]
                                              .split()])]
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
                position = sympy.Matrix([float(j) for j in index[line_offset +
                                                                 i].split()])
                AgBiIndex.append(position)
            print(f"Found {element[1]} positions for {element[0]}.")
            line_offset += element[1]
        case "Cu":
            assert element[1] == CU_AV
            for i in range(element[1]):
                position = sympy.Matrix([float(j) for j in index[line_offset +
                                                                 i].split()])
                CuIndex.append(position)
            print(f"Found {element[1]} positions for {element[0]}.")
            line_offset += element[1]
        case "I":
            assert element[1] == I_AV_OCC
            for i in range(element[1]):
                position = sympy.Matrix([float(j) for j in index[line_offset +
                                                                 i].split()])
                IIndex.append(position)
            print(f"Found {element[1]} positions for {element[0]}.")
            line_offset += element[1]
        case _:
            print("Syntax error on lines 6 and 7.")

# Open symmetries file
spacegroups = yaml.safe_load(open(args.symmetries, "r"))

# Look at the spacegroup number. We need to pick an element that will be in
# the minimum spacegroup, and then all other elements can be in equal or higher
# spacegroup

# Ag = 0
# Bi = 1
# Cu = 2
min_space_group_element = random.randrange(3)

match min_space_group_element:
    case 0:
        AgSpacegroup = args.spacegroup
        BiSpacegroup = random.choice(POSSIBLE_AG_BI_SG)
        CuSpacegroup = random.choice(POSSIBLE_CU_SG)
    case 1:
        AgSpacegroup = random.choice(POSSIBLE_AG_BI_SG)
        BiSpacegroup = args.spacegroup
        CuSpacegroup = random.choice(POSSIBLE_CU_SG)
    case 2:
        AgSpacegroup = random.choice(POSSIBLE_AG_BI_SG)
        BiSpacegroup = random.choice(POSSIBLE_AG_BI_SG)
        CuSpacegroup = args.spacegroup

# Randomly decide order of filling
filling_order = random.shuffle([0, 1, 2])

# Cycle through each and match statement
unused_ag_sites = AgBiIndex
unused_bi_sites = AgBiIndex
unused_cu_sites = CuIndex
used_ag_sites = []
used_bi_sites = []
used_cu_sites = []
while filling_order:
    current_element = filling_order.pop()

    match current_element:
        case 0:
            spacegroup = spacegroups[AgSpacegroup]
            symmetry_ops = [sympy.Matrix([x, y, z])]
            inv_symmetry_ops = symmetry_ops
            i = 1
            while i in spacegroup:
                M_i = sympy.Matrix(spacegroup[i]["M"])
                T_i = sympy.Matrix([0, 0, 0])
                if "T" in spacegroup[i]:
                    T_i = sympy.Matrix(spacegroup[i]["T"])
                symmetry_ops.append((M_i * symmetry_ops[0]) + T_i)
                inv_symmetry_ops.append((M_i.T * symmetry_ops[0]) - T_i)
                symopslen = len(symmetry_ops)
                i += 1
            if "+" in spacegroup:
                for vec in spacegroup["+"]:
                    vector = sympy.Matrix(vec)
                    for i in range(symopslen):
                        symmetry_ops.append(symmetry_ops[i] + vector)
            # Now we need to remove all whole number constants from each
            # component
            remove_whole_number_constants(symmetry_ops)
            # Num. of overlapped sites = Num. of groups needed * num. of ops in
            # that group - num. of sites to fill.
            multiplier = 1
            while multiplier * len(symmetry_ops) > AG_OCC:
                multiplier += 1
            overlapping_sites = multiplier * len(symmetry_ops) - AG_OCC
            # Now we will try and seed and grow each origin. If a collision or
            # an error is detected, the attempt for the element is scrapped
            # (((?))) and starts over from the top.
            attempts = 0
            while attempts < ATTEMPT_CREATION_TIMEOUT:
                # Need to do this to make sure that the list of available sites
                # is updated
                unused_ag_sites = unused_bi_sites
                failed = False
                num_groups = 0
                while num_groups < multiplier:
                    origin = random.choice(unused_ag_sites)
                    point_set = [op.subs([(x, origin[0]), (y, origin[1]),
                                          (z, origin[2])]).simplify()
                                 for op in symmetry_ops]
                    remove_whole_number_constants(point_set)
                    for loc in point_set:
                        # Check to see if it's in the list
                        if loc in unused_ag_sites:
                            unused_ag_sites.remove(loc)
                            used_ag_sites.append(loc)
                        else:
                            failed = True
                            break

                    num_groups += 1
                    # now we need to check the overlapping sites, iterate
                    # through all of the existing possible combinations of
                    # overlapping points, find their possible orgins, and then
                    # pick one of those potential origins and fill out the
                    # remaining points if they are unoccupied. If they are
                    # occupied, try the remaining possible origins before
                    # declaring it failed and starting over.
                    if multiplier > 1 and overlapping_sites > 0:
                        subsets = list(itertools.permutations(
                                       used_ag_sites), overlapping_sites)
                        num_subsets = len(subsets)
                        possible_origins = []
                        for i in range(num_subsets):
                            # systematically assign each point in the subset to
                            # a point in the set of inverse operations and try
                            # to derive a matching origin that is within the
                            # set of possible atomic sites.
                            inv_op_subs = list(itertools.permuatations(
                                               inv_symmetry_ops),
                                               overlapping_sites)
                            # Remove so that we don't get the original origin
                            # in the set of new possible origins.
                            inv_op_subs.remove(i)
                            for inv_op_sub in inv_op_subs:
                                # Need to now iterate through each point in
                                # each subset and use it to find its possible
                                # origin
                                poss_origin = []
                                for j in range(len(subsets[i])):
                                    poss_origin.append(inv_op_sub[j].subs([
                                        (x, subsets[i][j][0]),
                                        (y, subsets[i][j][1]),
                                        (z, subsets[i][j][2])]).simplify())
                                # Check to see if all points in poss_origin are
                                # the same
                                remove_whole_number_constants(poss_origin)
                                if listIsAllIdentical(poss_origin):
                                    possible_origins.append(poss_origin[0])
                        # If number of possible origins is 0, then mark as
                        # failed and break
                        if len(possible_origins) == 0:
                            failed = True
                            break
                        elif len(possible_origins >= multiplier - num_groups):
                            new_origins = random.sample(possible_origins,
                                                        multiplier -
                                                        num_groups)
                            for org in new_origins:





                if failed:
                    attempts += 1
                    continue
