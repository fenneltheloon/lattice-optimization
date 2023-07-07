import yaml
import argparse

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
for spacegroup in input:
    if 'a' in spacegroup:
        for subgroup in spacegroup:
            parse
    else:

