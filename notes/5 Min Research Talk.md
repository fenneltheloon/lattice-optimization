---
class: invert
paginate: true
inlineSVG: true
marp: true
---
<style>
  :root{
    --color-fg-default: #B0DFB4;
    --color-canvas-default: #0F1711;
  }

  h1{
    color: #AF4B34;
  }

  h2{
    color: #B27A59;
    align: "center";
  }

  h3{
    color: #6DA67B
  }

  img{
    display: block;
  }

  footer{
    color: #83A686;
  }
  
</style>

<style scoped>
  img[alt="utoledo"] {
    position: absolute;
    bottom: 5%;
    right: 5%;
    scale: 85%
  }
  img[alt="nsf"]{
    position: absolute;
    bottom: -73.9%;
    right: -13%;
    scale: 10%;
  }
</style>

# Optimizing Lattice Energy in Site-Disordered $\text{Cu}_2\text{AgBiI}_6$

Ethan Meltzer, Oberlin College
*Dr. Sanjay Khare, Dr. Richard Irving, Victor Barone*
**UToledo REU in Physics 2023**

![nsf](./NSF_Official_logo_High_Res_1200ppi.png)
![utoledo](./UToledo_HORZ_Logo_Reverse.png)

---
<style scoped> 
  img[alt="SEM"]{
    position: absolute;
    left: 8%;
    top: 30%;
    scale: 140%
  }

  h2{
    position: absolute;
    top: 10%;
    left: 40%
  }

  ul{
    position: absolute;
    width: 50%;
    right: 5%;
    top: 20%
  }
</style>

## Background

- Lead-free semiconductor synthesized at University of Liverpool in 2021 has promising applications in photovoltaics: simulated PCE of 30.2%, near-onset absorption coeff. of $1.0 \times 10^5\text{ cm}^{-1}$
- Initial research focused on synthesis and properties, simulations of internal structure using VASP performed serially, more computing power could result in more accurate structural models.
- Worth researching: better knowledge of internal structure nessecary to optimize solar cell design

![SEM](Cu2AgBiI6_SEM.png)

<!-- footer: "*Harry C. Sansom et al.\nJournal of the American Chemical Society 2021 143 (10), 3983-3992 DOI: 10.1021/jacs.1c00495" -->

---

![bg 80%](./Cu2AgBiI6_slide.png)


---
<style scoped>
  h2{
    position: absolute;
    left: 30%;
    top: 10%;
  }
</style>

## Combinatoric Complexity

How can we efficiently find the global minimum of a discrete function with unpredictable behavior and a very large finite domain?

$${108 \choose 18}\text{Cu} * \left[{27 \choose 9} * {18 \choose 9}\right]\text{Ag/Bi} = 3.173 * 10^{31}\text{ configurations}$$

### Big number
- $\text{TB} = 10^{12}$ bytes, would need 4 quintillion 1 TB storage drives to represent each configuration with 1 bit
- In microns, roughly the diameter of the observable universe

<!-- footer: "" -->

---
<style scoped>
  img[alt="flow"]{
    position: absolute;
    left: 10%;
    top: 30%;
    scale: 150%
  }

  h2{
    position: absolute;
    top: 8%;
    left: 30%;
  }

  ul{
    position: absolute;
    width: 50%;
    right: 5%;
  }
</style>

## Genetic Algorithmic Approach

- Converges on minimum while only looking at a small sample of the possible configurations
- Individual simulations easily parallelizable, can run ~50 simultaneously on UToledo servers compared to one-at-a-time
- Evaluating efficacy in this field is an active research area, especially with irregular materials

![flow](https://mermaid.ink/img/pako:eNplUstOwzAQ_JWVqxKQUqmtBAUjITUJBw6cWnFJOCzJGqw6NrIdoKD-O05S-iIHx56Z9a7G88NKUxHjbDj8KTSA1NJz6LYAkX-jmiIO0Qs6iuJD9AmtxBdFLtrJA_VuZY12nRplbFs3SJLp5fT6r3SvWNKX36uEEP8libEV2b1olo7Dd6BTUtOens-yZJ4c0I5Ko6ujacbjq8nRFZ6sl0eSdpSe3rS_sGyGw0IXWijzWb6h9bDM2nMrmecPwS-JSn6jl0Y_c86xp5J8QYrKEzTNU2ucMx9kD9Asf2z86QX35_mSbC11T1z0zLYvnEEGo9EdJNtu3SEN8P22UQfsBi0VOpeRAAQhleKDZDqbX97E4Lw1K-Jb9yCGsnWCw2AsJrPJ5LYvD06vFn6tCCoS2Ch_UsdiVodZUVYhSV0aCtalpGA8bMMjrAoWnAw6bLxZrHXJuLcNxax5r9BTJvHVYs24QOUCSpX0xj720ewSuvkFe83MEQ?type=png)

---
<style scoped>
  img[alt="utoledo"] {
    position: absolute;
    bottom: 5%;
    right: 5%;
    scale: 85%
  }
  img[alt="nsf"]{
    position: absolute;
    bottom: -73.9%;
    right: -13%;
    scale: 10%;
  }
</style>

# Thank you!

*emeltze@rockets.utoledo.edu*


![nsf](./NSF_Official_logo_High_Res_1200ppi.png)
![utoledo](./UToledo_HORZ_Logo_Reverse.png)

---
## Acknowledgements and References

**Research Team:** Dr. Sanjay Khare\*, Dr. Richard Irving\*, Victor Barone\*
\
**Highly Absorbing Lead-Free Semiconductor Cu2AgBiI6 for Photovoltaic Applications from the Quaternary CuI–AgI–BiI3 Phase Space**
*Harry C. Sansom, Giulia Longo, Adam D. Wright, Leonardo R. V. Buizza, Suhas Mahesh, Bernard Wenger, Marco Zanella, Mojtaba Abdi-Jalebi, Michael J. Pitcher, Matthew S. Dyer, Troy D. Manning, Richard H. Friend, Laura M. Herz, Henry J. Snaith, John B. Claridge, and Matthew J. Rosseinsky*
Journal of the American Chemical Society 2021 143 (10), 3983-3992
DOI: 10.1021/jacs.1c00495 

<!-- footer: "* University of Toledo Department of Physics" -->

---

## First generation
- Some correlation between crystal symmetry/regularity and lattice energy in similar materials, many exceptions
- Skewing the first generation of configurations towards highly symmetric (high space group) configurations could lead to a faster convergence on a minimum.
- Accomplish this by binning the randomly generated first generation
  - Each bin is equal size but
  - Number of space groups represented in each bin varies

![bg right:35% 90%](./space_group_ex.png)

<!-- footer: "" -->

---
<style scoped>
  li{
    font-size:0.95rem;
  }
</style>

## Generating child configurations
- Configs for future generations are generated from the best of the previous generation
- Crossover: site filling is determined by indexing the occupied sites of the parents and selecting at random
- Mutation: A few occupied atomic sites in the child configuration will be swapped with ones chosen at random, most often resulting in an atom switching with a vacancy.

![bg right:50% 80%](./ga-convergence.png)