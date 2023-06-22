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
  }

  h3{
    color: #6DA67B
  }
  
</style>

# Optimizing Lattice Energy in Irregular CM

Ethan Meltzer 
**UToledo REU 2023**

---
## Background

- New lead-free semiconductor $\text{Cu}_2\text{AgBiI}_6$ synthesized at University of Liverpool has promising applications in photovoltaics
- Initial research focused on expirimental properties, simulations of internal structure were unoptimized and worth further investigation
- Worth researching: if we're going to put this into a solar panel, we should know its structure!

![bg left:40% 95%](Cu2AgBiI6_SEM.png)

<!-- footer: Journal of the American Chemical Society 2021 143 (10), 3983-3992 DOI: 10.1021/jacs.1c00495 -->

---

![bg 85%](./Cu2AgBiI6_slide.png)


---

## The problem

How can we efficiently find the global minimum of a discrete function with unpredictable behavior and a very large finite domain?

$${108 \choose 18}\text{Cu} * \left[{27 \choose 9} * {18 \choose 9}\right]\text{Ag/Bi} = 3.173 * 10^{31}\text{ configurations}$$

### Big number
- $\text{TB} = 10^{12}$ bytes, would need 4 quintillion 1 TB storage drives to represent each configuration with 1 bit
- In microns, roughly the diameter of the observable universe 🪐🌌

<!-- footer: "" -->

---

## My approach

- Genetic algorithim converges on minimum while only looking at a small sample of the possible configurations
- Easily parallelizable, can run as many simulations as CPU threads available at once
- Use in this field is an active research area, especially with irregular materials

![bg left:40% 95%](https://mermaid.ink/img/pako:eNpdkEFrwzAMhf-KUGGnFEbYWuZBIYk72KGn9hbvIBxlNXXsYTsbW-l_n9eGUaqT9EnoPd4Rte8YBfbWf-k9hQQ7qZxykKtqX51Jhqz5oWS8exNC0GVVt1u2rG9o0zbBx-g_OVxR2W7GdPtg3e44DMZd80kV7kDCfL6CetI6D03G60nmDP5taksxSu6BoDfWilldLqvHpwJiCv7AAmYLWS2WdQHaWx_yXFYP9-XLMxY4ZBNkuhzA8e-ZwrTngRWK3HYUDgqVO-U7GpPffjuNIoWRCxw_OkosDb0HGlD0ZGOm3Jnkw-aS6DnY0y9vL2vA?type=png)

---

# Thank you!

*emeltze@rockets.utoledo.edu*

---

## First generation
- Some correlation between crystal symmetry/regularity and lattice energy in similar materials, many exceptions
- Skewing the first generation of configurations towards highly symmetric (high space group) configurations could lead to a faster convergence on a minimum.
- Accomplish this by binning the randomly generated first generation
  - Each bin is equal size but
  - Number of space groups represented in each bin varies

![bg right:35% 90%](./space_group_ex.png)

---
<style scoped>
  li{
    font-size:0.95em;
  }
</style>

## Generating child configurations
- Configs for future generations are generated from the best of the previous generation
- Crossover: site filling is determined by indexing the occupied sites of the parents and selecting at random
- Mutation: A few occupied atomic sites in the child configuration will be swapped with ones chosen at random, most often resulting in an atom switching with a vacancy.

![bg right:50% 80%](./ga-convergence.png)