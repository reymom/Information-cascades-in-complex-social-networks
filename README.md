# Information-cascades-in-complex-social-networks
My first project involving theory of complex systems, back in 2016.

I modeled the spreading of information through a Integrate-and-Fire-like system (as in neurons spiking dynamics) that allows us to reproduce experimental data obtained from Twitter, where it is easy to find the two regimes (calm stage and turbulent one showing large cascades for the propagation of certain tweets) and the phase transition separating them. I do other kinds of analysis using theory of Complex Systems, as I analyze the role of the nodes in the spreading phenomena.

I tried to upload here some basic programs, although I ended up having almost 40, the dynamics is performed in many programs, and many others just open data saved in text and make Figures. Basically, I have programs that performs the algorithm for the dynamics in a random graph (Erdos-Renyi) and others in a scale-free (Barabasi-Albert). Then there are others that extract and analize the roles and relate the dynamics to the individual features of the nodes.

The comments in the programs are in Spanish, sorry for that, as well as for the bad organization of the programs, since it was my first big work. Now I would only have one program for the functions defining the dynamics and the extraction of networks and its features, and other programs taking that functions and applying to take results and Figures. Nevertheless, I think it is interesting to read the PDF and see how the dynamics works in some program.

## Material
The programs (.py) for doing the simulation and extract the results for the dynamics, including the phase-state:
- CascadeSize_barabasi.py : one of the main programs where the dynamics is performed using a Barabasi-Albert network (scale-free). From here I extract the results in order to plot the cascades size distribution and cumulatives, as well as the cascade sizes in relation with the node's connections.
- Cascade_BA_ROLES.py : main program to perform the same dynamics and doing the analisis of the roles for the networks

The article where I explain in detail (but I little bit briefly, as the maximum lenght of the paper for the subject was 5 pages).
Here you can find all references and understand what I did and its applications to real social networks.
