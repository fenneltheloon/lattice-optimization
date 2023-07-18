import pymatgen.io.vasp
import pymatgen.symmetry.analyzer

file_path = "ag.vasp"
R_TOL = 0.5
A_TOL = 5.0

# Calculate and append spacegroup to the start of the file
poscar = pymatgen.io.vasp.inputs.Poscar\
    .from_file(file_path, check_for_POTCAR=False, read_velocities=False)

# TODO: figure out why this is only returning 1. Ran 40k+ attempts, only
# returned 1 ever. Am I just not scanning enough input or is there actually
# a problem with the system?
spacegroup = pymatgen.symmetry.analyzer.\
    SpacegroupAnalyzer(poscar.structure, symprec=R_TOL,
                       angle_tolerance=A_TOL).get_space_group_number()

print(spacegroup)
