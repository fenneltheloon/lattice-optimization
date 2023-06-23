# first-gen-filler

Will need to parse POSCAR format into the varaibles that spglib uses e.g. :

```python
lattice = [[1.0, 0.0, 0.0], # a
            [0.0, 1.0, 0.0], # b
            [0.0, 0.0, 1.0]] # c
positions = [[0.0, 0.0, 0.0], # Al
            [0.5, 0.5, 0.0], # Ni
            [0.0, 0.5, 0.5], # Ni
            [0.5, 0.0, 0.5]] # Ni
numbers = [1, 2, 2, 2]        # Al, Ni, Ni, Ni
```

Example POSCAR:
```
Cubic BN
3.57
0.0 0.5 0.5 #a
0.5 0.0 0.5 #b
0.5 0.5 0.0 #c
B N
1 1
Direct
0.00 0.00 0.00 # B
0.25 0.25 0.25 # N
```

We're going to want to specify how the generatred POSCARs should identify themselves. This should be in the first line:

There are 63 Cu sites and 27 Ag/Bi sites.

First line should be:
Ag-n1-n2-n3...-n9_Bi-n1-n2-n3...n9_Cu-n1_n2_n3...n18

Name of file that contains all indices should be called `INDEX.vasp` and it should be in the root of the directory that is passed into the program.

## Formula for 