## Spherical cluster method for ground state determination of site-disordered materials: application to $\textup{Ag}_{x}\textup{Bi}_{y}\textup{I}_{x+3y}$
*Victor T. Barone, Blair R. Tuttle, Sanjay V. Khare*

- Is there any way to experimentally determine the internal structure of the lab-grown crystal? X-ray crystallography has probably been tried, but why has it failed?

> Choosing the explicit arrangements of silver, bismuth and vacancies to occupy these sites is a combinatorially difficult problem, e.g. the 294 atom case of AgBi2I7 has over $10^{100}$ possible solutions.
- This does seem like a discrete problem with discrete solutions, but is there any reason that we can't use a probabilistic approach that instead gives *likelihoods* of atoms in each position? Would looking at it through that lens perhaps simplify the problem? Would it also make the results potentially more representative of the irregularity that is observed in real life?

- [Simulated annealing](https://en.wikipedia.org/wiki/Simulated_annealing)
$$P = \begin{cases}
	\exp \left[-\left(E\left(S_j\right) - E\left(S_{j-1}\right)\right) / \tau_{j}\right] & \text{if }E\left(S_{j-1}\right) < E\left(S_j\right)\\
	1 & \text{otherwise}
\end{cases}$$
> Ohio Supercomputer Center’s Owens supercomputing cluster
- OSCOSC, heehee

## Highly Absorbing Lead-Free Semiconductor $\text{Cu}_2\text{AgBiI}_6$ for Photovoltaic Applications from the Quaternary $\text{CuI}$−$\text{AgI}$−$\text{BiI}_3$ Phase Space
*Harry C. Sansom, Giulia Longo, Adam D. Wright, Leonardo R. V. Buizza, Suhas Mahesh, Bernard Wenger, Marco Zanella, Mojtaba Abdi Jalebi, Michael J. Pitcher, Matthew S. Dyer, Troy D. Manning, Richard H. Friend, Laura M. Herz, Henry J. Snaith, John B. Claridge, and Matthew J. Rosseinsky**

> Since the proposed double-perovskite $\text{Cs}_2\text{AgBiI}_6$ thin films have not been synthesized to date, $\text{Cs}_2\text{AgBiI}_6$ is a valuable example of a stable $\text{Ag}^+$ / $\text{Bi}^{3+}$ octahedral motif in a close-packed iodide sub lattice that is accessed via the enhanced chemical diversity of the quaternary phase space.

Savory, C. N.; Walsh, A.; Scanlon, D. O. Can Pb-Free Halide Double Perovskites Support High-Efficiency Solar Cells? ACS Energy Lett. 2016, 1 (5), 949−955.

- It sounds like the proposed ideal material has more desirable electrical properties. We won't be dealing with it, but do we know how similar/dissimilar our material is to the ideal? 
- [Like what even is a Perovskite](https://www.princeton.edu/~cavalab/tutorials/public/structures/perovskites.html)

> that is accessed via the enhanced chemical diversity of the quaternary phase space.

- What does this mean?

> To gain some insight into the nature of the electronic transitions underlying optical absorption, we have performed density functional theory calculations on ordered structural models of Cu2AgBiI6 based on the refined experimental disordered structures.

- How are the calculations that we are doing different? They have ordered structural models already, is that not what we are trying to obtain?

