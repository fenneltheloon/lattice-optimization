#set page(paper: "us-letter")
#set text(font: "New Computer Modern")
#set par(justify: true)
#show link: underline
#show link: set text(fill: blue)

#align(center)[#text(size: 16pt)[*Minimizing Lattice Energy in Site-Disordered Cu#sub[2]AgBiI#sub[6]*]]
Ethan Meltzer#super[a], Mr. Victor T. Barone#super[b], Dr. Sanjay V. Khare#super[b], Dr. Richard E. Irving#super[b]

#text(size: 10pt)[#super[a] Oberlin College Department of Computer Science#linebreak()
#super[b] University of Toledo Department of Physics]

#align(center)[*Abstract*]
Cu#sub[2]AgBiI#sub[6] is a new thin-film solar cell site-disordered semiconductor candidate synthesized by the University of Liverpool in 2021.#super[1] This research aims to find minimum-energy configurations of its crystal structure using an evolutionary algorithmic approach and VASP _ab-initio_ calculations of lattice energy to determine suitability. We employ the USPEX#super[2] structure prediction algorithim as well as our novel approach which focuses on the site-disordered nature of the material and on intentionally biasing the first generation of the evolutionary process towards lower-energy configurations by selecting for higher-order space groups. By comparing both of these methods, we aim to both reinforce our confidence in finding the global minimum-energy configuration and evaluate the effectiveness of our novel evolutionary approach.

#align(center)[*Background*]
This new material is a promising candiate for thin-film solar cell applications due to its high absorption coefficient of $1.0 * 10^5 space #text[cm]^(-1)$ in visible light, ideally competing with or outperforming current-gen materials like CdTe or Si-based cell technology.#super[1] In order to engineer high-efficiency solar cells using this material, further research into the internal crystal structure of the material beyond what the initial expirimental inquiry that verified stoichiometry and the positions of lattice sites using X-ray powder diffraction techniques is necessary.

#align(center)[*Methods*]
USPEX is a very effective crystal structure predictor, and we will be using it as a point of comparison against our new approach. By specifying interatomic distance, stoichiometry, and lattice vectors it will find minimum-energy structures with high accuracy. Despite this, it does not consider the unique challenges that site-disordered crystals pose, and is more well-suited for highly-symmetric materials.

Our approach focuses on intentionally biasing the first generation of the evolutionary process. By starting with a selected sample of low-energy configurations using some method that is less computationally intensive than the DFT simulations performed by VASP or similar, we aim to jumpstart the process and significantly reduce the number of generations and simulations needed to converge on a minimum.

Our initial approach was to randomly generate configurations of the crystal using a VASP5 POSCAR file containing all of the atomic sites in a 3x3x1 lattice cell, and sort those configurations by their crystallographic space group, placing them into bins of equal size, where each bin contained a different number of space groups. By including more space groups in the lower-numbered bins and less space groups in the higher-numbered bins, we effectively apply a bias in the initial population towards configurations with high space groups. Research in Dr. Khare’s lab has suggested that the population of high-symmetry configurations has a larger frequency of low-energy configurations than low-symmetry high-disorder configurations do. If we select for high-symmetry configurations to initialize the popualtion, hopefully they will begin with a low median energy and convergence will be faster. We developed a fully parametrized approach to applying this bias, using the area under a bell curve as a starting point. The distribution can be described with the following system of equations:

$ B_i = round(cases(a (Chi ((z i)/n)) / (Chi (z)) "," z > 0, a i/n "," z = 0, a (1 - (Chi ((z i)/n))/(Chi (z))) "," z < 0)) $
$ Chi (x) = integral_0^x exp (- t^2/2) d t $

Where $B_i$ is the largest space group that each consecutive bin $i$ will contain, $a$ is the total number of space groups (230 for a three-dimensional crystal), $n$ is the number of bins that will be divided into, and $z$ is the bias factor. The more positive $z$ is, the more aggressive the bias will be towards high space groups, and similarly the more negative $z$ is, the more aggressive the bias will be towards low space groups. The idea is that we bound an area underneath a Gaussian (determined by $z$), divide the input space into equal parts, and then compare the area of the entire bound ($Chi (z)$) to the area of $i$ parts ($Chi ((z i) / n)$). This gives us a fraction from 0 to 1 which we then scale by $a$ and round off to give a discrete space group number. In the negative $z$ case, we simply take the "one minus" inverse of this fraction, which will switch which edge is being biased towards, and when $z = 0$ the bias dissappears and the function is linear.

For a distribution that selects for a specific set of space groups (biased towards the center), a similar distribution is defined. Let $p$ and $q$ be the lower and upper bounds of the space group range to be biased towards (so the mean of the Gaussian is centered between them). We will define a new inverse distribution $Psi$:

$ Psi (a, b) = b - a + integral_b^a exp(-(t^2)/2) d t $

Opposite to a Gaussian, the density function this corresponds to outputs 0 at input 0 and approaches 1 at large magnitude input. For the sake of legibility, we will define some useful terms for representing the statistical $z$-values of space group 0 and space group $a$, $0^*$ and $a^*$ respectively.

$ 0^* = -(q+p)/(2z(q-p)) $
$ a^* = a/(z(q-p)) + 0^* $

$B_i$ is then given with:

$ B_i = round(a((Psi (0^*, (i(a^* - 0^*))/n + 0^*)) / (Psi (0^*, a^*)))) $

We ran `first-gen-filler.py` to generate configurations at random and sort them into their corresponding bins using a positive-$z$ edge-biased distribution.

#align(center)[*Initial Results*]
We generated \~50k configurations and expected about 0.5% of them to be "high-symmetry" (with a space group > 1) or approximately 250 high-symmetry configurations, but we were unable to generate a single high-symmetry configuration. We realized that the shape of the lattice was trigonal, and even ignoring that, due to the stoichiometry of the $3 * 3 * 1$ cell that we were working with, the vast majority of space groups were impossible to acheive from a combinatoric standpoint. We then began an investigation into the specific space groups that were possible, with the goal of being able to manually generate those configurations to get around the problem of not being able to generate these configurations at random. We aimed to use our understanding of the specific material to combinatorically generate these structures, which requires much less power than _ab-initio_ simulation at the expense of research time and a more complex generation algorithim.

#align(center)[*Manual Generation*]
To verify which space groups were feasible to attempt to generate, a few requirements must be satisfied. First, the spacegroup of the entire crystal is the minimum of the spacegroups of the individual elemental sublattices. Secondly, any spacegroup that has more symmetry operations than we have atoms of a specific element (9 Ag, 9 Bi, and 18 Cu for a $3*3*1$ cell) is out of contention, as we cannot possibly map atoms to each required symmetry operation. Additionally, any space group with a number of operations that is co-prime to the number of atoms that a particular element has is also out of contention, as there is no possible way to overlap symmetry sets to have one element non-overlapping. However, a symmetry set with fewer operations than there are atoms of a specific element that shares a factor with the number of atoms of that element is possible as long as that group is open---where points inside a symmetry set can map outside of the set when used as the origin. All of the space groups that qualified, trigonal groups 143 - 161 were open, so we focused on constructing an algorithim that would generate configurations that fell into these space groups.

A detailed flowchart of the algorithim used is provided in `Final Presentation.odp`, the associated presentation to this report. The general idea is that the individual elemental sublattices are filled one at a time, with the complexity that Ag and Bi share a sublattice. The elements are assgined an order to be filled in, as well as a specific spacegroup the sublattice will be generated as, with one of the elements being the minimum, input-specified group. Then symmetry groups are seeded and grown one at a time, with an orgin being selected at random and using the defined symmetry operations to fill the rest of the points. If symmetry groups need to overlap to satisfy the stoichiometry of the cell, then subsets of the occupied sites and the inverses of the group's symmetry operations are generated and convoluted to generate possible alternate origins, which are then slected at random and verified.

#align(center)[*Continued Research*]
This project is currently unfinished. The immediate next steps include preparing and executing a USPEX simulation to verify its validity and effectiveness for this material, completing the implementation of the manual genertaion algorithim in Python and using it to generate a first generation of configurations to simulate using VASP. The code for our evolutionary algorithim is also currently unwritten, but should be straightforward to implement. The suitability criteria for each generation will likely be simply the lattice energy that VASP reports, and the cutoff will be a bottom percentile of energies that likely depends on the initial generation size and current generation, becoming more and more selective as the generations increase. University of Toledo Department of Physics has generously granted this project the server space to be able to run these required simulations. The novel algorithim should be run multiple times to confirm results and to tweak its many parameters. Once that is done, a comparison of the computation costs associated with both USPEX and the novel algorithim should be performed to evaluate its effectiveness at addressing site-disordered this site-disordered material. Work should then be done if worthwhile on generalizing the codebase for the novel algorithim so that future site-disordered projects can take advantage.The final goal is to report both the minimum-energy structures that are found as well as the effectiveness of the novel algorithim.

#align(center)[*Supplementary Material*]
All code and media generated for the purposes of this project, including the files mentioned above are available in a public github repository located at this link: https://github.com/captainbanaynays/lattice-optimization

#align(center)[*References*]
#super[1] Sansom et al. _Highly Absorbing Lead-Free Semiconductor Cu#sub[2]AgBiI#sub[6] for Photovoltaic Applications from the Quaternary CuI−AgI−BiI#sub[3] Phase Space._
Journal of the American Chemical Society 2021 143 (10), 3983-3992
DOI: 10.1021/jacs.1c00495

#super[2] Glass et al. _USPEX – evolutionary crystal structure prediction._ Computer Physics Communications 175 (2006) 713-720 DOI: 10.1016/j.cpc.2006.07.020
