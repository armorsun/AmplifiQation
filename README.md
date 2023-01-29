# pyROUTE

```pyROUTE``` is a user-centric route optimization and itinerary scheduling solution developed by AmplifiQation.

Adaptable, and engineered for scalability, ```pyROUTE``` delivers quantum enhanced tools for:

- Evening and hang-out planning;
- Vacation and business-trip scheduling;
- and logistics and supply-chain management.

```pyROUTE``` is available under the MIT license [here](/LICENSE).

# AmplifiQation

```pyROUTE``` was developed during MIT iQuHACK 2023 by the AmplifiQation team. More on iQuHACK 2023 [here](https://www.iquise.mit.edu/iQuHACK/2023-01-27).

[Michael Luciuk](https://www.linkedin.com/in/michael-luciuk/) (University of Toronto)
[Chaitanya Kumar Mahajan](https://www.linkedin.com/in/chait27/) (University of Toronto)
[Kae-Yang Hsieh](https://www.linkedin.com/in/sunnyhsieh/) (Northeastern University)
[Veronica Lekhtman](https://www.linkedin.com/in/veronica-lekhtman-78a2a11b3/) (Northeastern University)
[Karishma Bhargava](https://www.linkedin.com/in/karishmabhargava-19142123a/) (Northeastern University)


# The Quantum Components

```pyROUTE``` leverage fundamental quantum computing principles to accelerate optimization.

## Random Number Generation

By preparing and measuring a Bell State, ```pyROUTE``` empowers the user with the truly random options.

## Quantum-enhanced TSP (travelling salesman problem) solver

By running the Dürr and Høyer algorithm [1] on precomputed Hamiltonian cycles, ```pyROUTE``` provides a quantum-enhanced routing optimizer.

[1] C. Dürr and P. Høyer, “A Quantum Algorithm for Finding the Minimum,” 1996. https://arxiv.org/abs/quant-ph/9607014.

# Getting Started

## Pre-requisite
* Install [Docker](https://docs.docker.com/get-docker/) and [Docker-compose](https://docs.docker.com/compose/install/)

## Launch

```
docker-compose build
docker-compose up -d
```

# Example Usage

```
curl http://localhost/random
curl http://localhost/PyROUTE
```

# Future Work

While ```pyROUTE``` serves as a value proof-of-concept, the AmplifiQation has yet to:

- Enhance ```pyROUTE``` with real-world data from Google Maps API;
- Integrate temporal data and opening times into the core solver;
- or, further explore quantum graph algorithms are their respective speedups;
- build a graphical user interface.


# iQuHACK 2023

iQuHACK is a faced-paced, valuable learning experience accessible to all levels of quantum experience. The AmplifiQation team highly recommends you consider applying for further.

iQuHACK was made possible by a dedicated organizing committee and generous sponsor supports.

# Issues

Issues should be reported to the issues board [here](https://github.com/armorsun/AmplifiQation/issues).
