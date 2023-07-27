# Spacegroup sym

Top-level-list: each space group  
- Plus vector(s): for each plus vector, duplicate all numbered symmetry
operations and apply plus vector to each
- Individual symmetry operations
    - Matrix
    - Translation vector


For each space group:

1. Create a list of points from the symmetry ops and the plus vectors
2. Plug each into the symmetry ops again, apply mod operation to remove whole
    number constants and then cross-reference with original list to see if each
    new point exists in the original
3. If spacegroup is "closed", check to see if Cu/Ag/Bi sites are a strict
    multiple of the number of symmetry ops. If open, check to see if they are
    noncoprime. If that condition is met, then print the spacegroup subnumber
    to stdout.

## next steps

Okay so now we write the generation file
- Make sure that we have a function that will take a subset of points that are
mapped onto and see if we can get alternate origins

Plan: if the space group has 3 operations, then we will just pick 3 orgins that
do not occupy the same spots

If we have a 6-point group, then we will need to generate one group of points,
then try to find origins that map onto a subset of those points.

Keep track of what symmetry operation generated each point, then iterate
through the other options (will be 5! possibilities for each set of 3 points,
and 6 choose 3 = 20 different sets so will be 2400 operations per initial 
symmetry). 

### Algorithim

Iterate through tuples of symmetry operations for 3 points
For each point:
- Undo the translation vector
- Multiply by the inverse of the rotation Matrix

log the result and repeat for the other two points
If we get that all three points map to the same origin, save that point

Check to see if the origin is in the proper lattice that we are examining

Repeat until we have all possible origin points for that three point pair

Do this symbolically? if possible so we don't have to do it every time.

143-161 are the only ones that we are looking at for Ag/Bi - 143-146 are 3 and 147-161
are 6.

Copper: Max is 221, all groups underneath with less than 18: 143-190, 195, 198  

Not true - these are the only space groups that we will need for Ag/Bi. Copper
will need to be able to use any space group it can - which is pretty much any
group that has 18 points or less. Will need to write down some of the higher
order space groups into the yaml file to process. And then make sure the Cu
code is updated.

Pick one of Ag/Bi/Cu to be the min space group, then all others will greater
than or equal to as long as they are valid.

If group is open and gcd of number of ops in formula and number of ops in
spacegroup is not one AND space group has number of ops less than or equal to
number of sites that will be filled by that sublattice, then can use.

If number of space group symops not a factor of number of sites,
then find smallest multiple that is greater than the number of sites, find how
many overlap, and see if that divides evenly between the number of symmetric
units.

If it is, then multiply and make sure they do not overlap.

Copper space group is 221, iodine is 225. Ag/Bi is 166.

## Algorithm for inverse

Read in index file, spacegroup yml

Read in all of the elements into sympy format

Decide filling order, randomize the spacegroup

Perform the filling operation for each spacegroup:
1. get the spacegroup from the YML file into sympy form
1. Figure out how many sites are needed left to fill, how many need to overlap. 

```
overlapping_sites = multiplier * len(symmetry_ops) - AG_OCC

```
1. Fill the first symmetry set
    - We need to be careful about checking the tolerances on each of the
        coordinates when doing this. Too strict and nothing will ever register,
        too loose and we'll get error accumulating.
1. Get all of the possible subsets of that set and subsets of the symmetry operations
with `itertools.permuations`
1. Permute the subsets together such that all possible pairs are generated
    except for the ones that coincide indices (so we don't get the same set of
    points back out.) For each of these pairs:
    1. Call a function that calculates a potential origin for these points
    On success, return point. On failure, return code.
    1. If no successes, fail the attempt and skip to the next. If there is
        a success, generate all of the points corresponding to that origin
        and ensure that they are all valid.
    1. Continue until we have the `multiplier` number of sites filled and
        number of sites filled is what it's supposed to be.
    1. Copy and save list as the final for element going into poscar, then if
        Ag/Bi, copy use sites over to other element.
1. Write the POSCAR file. Repeat for as many configurations as requested.

