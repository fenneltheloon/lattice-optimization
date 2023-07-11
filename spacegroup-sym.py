import yaml
import argparse
import sympy
import pdb

x, y, z = sympy.symbols('x, y, z')

parser = argparse.ArgumentParser(
        prog="Spacegroup Symmetry Finder",
        description="This script takes a dataset of spacegroups and their\
                listed symmetry operations and can determine whether or not\
                that spacegroup is closed under its symmetry. Start with an\
                origin point and use the symmetry operations to generate the\
                corresponding sites. Then use each of those sites as an\
                origin and see if the sites that they generate fall inside or\
                out of the initial set of points."
        )

parser.add_argument("-i", "--input", help="The input file. Must be a YAML\
        document containing spacegroup symmetry operations.")

args = parser.parse_args()

input = open(args.input, "r")
input = yaml.safe_load(input)

# Big ass for loop - determine symmetry operations
for spacegroup in input.items():
    if spacegroup[0] == 1:
        print(f"Group {spacegroup[0]} is closed")
        continue
    isClosed = True
    symmetry_ops = [sympy.Matrix([x, y, z])]
    i = 1
    while i in spacegroup[1]:
        M_i = sympy.Matrix(spacegroup[1][i]["M"])
        T_i = sympy.Matrix([0, 0, 0])
        if "T" in spacegroup[1][i]:
            T_i = sympy.Matrix(spacegroup[1][i]["T"])
        symmetry_ops.append((M_i * symmetry_ops[0]) + T_i)
        symopslen = len(symmetry_ops)
        i += 1
    if "+" in spacegroup[1]:
        for vec in spacegroup[1]["+"]:
            vector = sympy.Matrix(vec)
            for i in range(symopslen):
                symmetry_ops.append(symmetry_ops[i] + vector)
    # Now we need to remove all whole number constants from each component
    for op in symmetry_ops:
        for comp in op:
            const = sum([term for term in comp.as_ordered_terms() if
                        term.is_constant()])
            if const > 0:
                const = -sympy.floor(const)
            else:
                const = -sympy.ceiling(const)
            comp = comp + const
            op.simplify()
    # Now run each site through the same set of ops and see if we get the
    # same site back
    for op in symmetry_ops:
        # TODO: make sure that this will result in N vectors (okay bc will run N times)
        sym_op_alt = []
        compose = [(x, op[0]), (y, op[1]), (z, op[2])]
        for op2 in symmetry_ops:
            breakpoint()
            new_vec = sympy.Matrix([op2[0].subs(compose), op2[1].subs(compose),
                                    op2[2].subs(compose)])
            sym_op_alt.append(new_vec)
        # Remove all whole number constants again
        for op2 in sym_op_alt:
            for comp in op2:
                const = sum([term for term in comp.as_ordered_terms() if
                            term.is_constant()])
                if const > 0:
                    const = -sympy.floor(const)
                else:
                    const = -sympy.ceiling(const)
                comp = comp + const
                op.simplify()
        # Now check to see if all operations are contained within the original
        # list
        while isClosed:
            for op2 in sym_op_alt:
                if op2 not in symmetry_ops:
                    isClosed = False
                    break

        # Print whether or not the space group is closed
        if isClosed:
            print(f"Group {spacegroup[0]} is closed")
        else:
            print(f"Group {spacegroup[0]} is open")
