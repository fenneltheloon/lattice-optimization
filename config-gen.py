import sympy
import math
import random
import argparse
import sys
import yaml


# Needs to be a list of 3d-points of type sympy.Matrix (3d colun vector)
def list_crystal_mod(list):
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


def point_crystal_mod(point):
    for coord in point:
        const = sum([term for term in coord.as_ordered_terms() if
                    term.is_constant()])
        if const > 0:
            const = -sympy.floor(const)
        else:
            const = -sympy.ceiling(const)
        coord = coord + const
    point.simplify()


# Checks if the point is within a certain tolerance of any point contained
# within the list.
def is_point_in_list(my_point, my_list, tolerance):
    for list_point in my_list:
        distance = math.sqrt(((my_point[0] - list_point[0]) ** 2) +
                             ((my_point[1] - list_point[1]) ** 2) +
                             ((my_point[2] - list_point[2]) ** 2))
        if distance <= tolerance:
            my_point = list_point
            return True
    return False


# Checks if the points in list1 are within a certain tolerance of any points
# contained within the list2.
def is_list_in_list(list1, list2, tolerance):
    for my_point in list1:
        for list_point in list2:
            distance = math.sqrt(((my_point[0] - list_point[0]) ** 2) +
                                 ((my_point[1] - list_point[1]) ** 2) +
                                 ((my_point[2] - list_point[2]) ** 2))
            if distance <= tolerance:
                my_point = list_point
                break
        return False
    return True


class Element:
    def __init__(self, symbol, spacegroup_num, sites):
        self.symbol = symbol
        self.spacegroup_num = spacegroup_num
        self.sites = sites
        self.unused_sites = self.sites
        self.used_sites = []
        self.symmetry_ops = [sympy.Matrix([x, y, z])]
        self.inv_symmetry_ops = self.symmetry_ops
        self.spacegroup = spacegroups[self.spacegroup_num]
        i = 1
        while i in self.spacegroup:
            M_i = sympy.Matrix(self.spacegroup[i]["M"])
            T_i = sympy.Matrix([0, 0, 0])
            if "T" in self.spacegroup[i]:
                T_i = sympy.Matrix(self.spacegroup[i]["T"])
            self.symmetry_ops.append((M_i * self.symmetry_ops[0]) + T_i)
            self.inv_symmetry_ops.append((M_i.T * self.symmetry_ops[0]) - T_i)
            i += 1
        if "+" in self.spacegroup:
            for vec in self.spacegroup["+"]:
                vector = sympy.Matrix(vec)
                for i in range(len(self.symmetry_ops)):
                    self.symmetry_ops.append(self.symmetry_ops[i] + vector)
        # Now we need to remove all whole number constants from each
        # component
        list_crystal_mod(self.symmetry_ops)

    def gen_first_point_set(self, attempt_num):

        # Check for attempt timeout first
        if attempt_num >= ATTEMPT_CREATION_TIMEOUT:
            raise Exception("Attempt timeout reached.")

        origin = random.choice(self.unused_sites)
        temp_point_list = []
        for op in self.symmetry_ops:
            new_point = op.subs([(x, origin[0]), (y, origin[1]),
                                 (z, origin[2])]).simplify()
            point_crystal_mod(new_point)
            temp_point_list.append(new_point)
        if not is_list_in_list(temp_point_list, self.unused_sites):
            self.gen_first_point_set(attempt_num + 1)
        else:
            for point in temp_point_list:
                point


DIST_TOL = 0.00000001
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

# Randomize order of filling as well as what spacegroup is assigned to each
# element.

