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

## Algorithim for computing num. of space groups in each bin

Compute the values of each $B_i$ for the following series:

$$\sum_{i=1}^n{B_i} = a$$
where:
$$B_i = \text{round}\left[2a\left(\Phi\left(\frac{zi}{n}\right) - \Phi\left(\frac{z(i-1)}{n}\right)\right)\right]$$

$$\Phi(x) = \frac{1}{\sqrt{2\pi}}\int_0^x{\exp\left(-\frac{t^2}{2}\right)dt}$$

where:
- $B_i$ is the i-th bin
- $n$ is the total number of bins being divided into (positive integer)
- $a$ is the number of space groups (positive integer)
- $z$ is the number of standard deviations captured on the exponential curve (practically, will control how aggressively we will select for high space groups, the higher $z$ the more aggressive it is) (positive real)

for $B_n$, sum the values of the series so far including $B_n$ and adjust up or down to $a$ (should be $\pm 1$) due to rounding error.

Alternatively, just mark down
$$B_i = \text{round}\left[2a\Phi\left(\frac{zi}{n}\right)\right]$$

and let $B_n := a$, then when sorting just put any space group less than or equal to that upper value into that bin.