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

143-161 are the only ones that we are looking at - 143-146 are 3 and 147-161
are 6.
