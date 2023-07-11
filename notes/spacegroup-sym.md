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
