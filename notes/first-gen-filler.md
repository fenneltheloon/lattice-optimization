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
### In the edge-biased case

Compute the values of each $B_i$ for the following series where:
$$B_i = \text{round}\left[\begin{cases}
  a\frac{\Chi\left(\frac{zi}{n}\right)}{\Chi(z)} & ,z > 0\\
  a\frac{i}{n} & ,z=0\\
  a\left(1 - \frac{\Chi\left(\frac{zi}{n}\right)}{\Chi(z)}\right) & ,z < 0\\
  \end{cases}\right]$$

$$\Chi(x) = \int_0^x{\exp\left(-\frac{t^2}{2}\right)dt}$$

where:
- $B_i$ is the i-th bin
- $n$ is the total number of bins being divided into (positive integer)
- $a$ is the number of space groups (positive integer)
- $z$ is proportional to the number of standard deviations captured on the normal distribution (practically, will control how aggressively we will select for high space groups, the larger the magnitude of $z$, the more aggressive the selection)

**Note:** $\Chi(x)$ is a simplified form of $\Phi(x)$, the CDF of a standard normal distribution. The $\frac{1}{\sqrt{2\pi}}$ term is divided out and as such does not need to be computed.

### in the non-edge-biased case
Let's say that we have a specific space group that we want to bias towards. We can then use something like this:

Let $p$ and $q$ be the lower and upper bounds of the desired range to bias towards (so the mean $\mu$ of the distribution is centered between them). Define a new inverse distribution $\Psi$:
$$\Psi(a,b) = b - a + \int_b^a{\exp\left(-\frac{t^2}{2}\right)dt}$$

Opposite to a bell curve, this density plot is 0 at input 0 and approaches 1 at large magnitude input.
We'll also define some useful terms that represent the z-values of space group 0 and space group $a$, $0^*$ and $a^*$ respectively:

$$0^* = -\frac{q+p}{2z(q-p)}$$
$$a^* = \frac{a}{z(q-p)} + 0^*$$

We then have:
$$B_i = \text{round}\left[a\left(\frac{\Psi(0^*, \frac{i(a^* - 0^*)}{n}+0^*)}{\Psi(0^*, a^*)}\right)\right]$$

where $a$, $i$, and $n$ mean the same the same thing, and $z$ this time refers to how far apart $p$ and $q$ are on the distribution (when $z = 1$, $p$ and $q$ are 1 standard deviation apart). Similarly to before, the higher $z$ is, the more aggressively the distribution will be biased towards the range we are selecting for. Because the distribution density function is flipped, the value of $z$ is replaced by its multipliciative inverse to keep its behavior consistent. (So $z = 2$ means $p$ and $q$ are 0.5 std apart).

## First Run
Traceback: zip object has no length. Look at parsing the element names form the
INDEX file