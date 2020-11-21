import numpy as np
import matplotlib.pyplot as pl
from scipy.spatial import cKDTree
import scipy
import utilities as ut
import moves
import tqdm
import sys

bignumber = np.inf
epsilon_1 = 0.5
epsilon_2 = -1.0
r1 = 1.0
r2 = 2.0
r3 = 2.2
parameters = [r1, r2, r3]

# N = 255
L = 11.090369
T = 0.6320
beta = 1. / T
delta = 0.1
iterations = 10000


def twosteps(x, parameters):
    r1, r2,r3 = parameters[0], parameters[1], parameters[2]
    u = np.zeros_like(x)
    u[x <= r1] = bignumber
    u[(x>r1)*(x<=r2)] = epsilon_1
    u[(x<=r3)*(x>r2)] = epsilon_2

    return u


# view interaction
# x = np.linspace(0,3,10000)
# pl.plot(x, twosteps(x,parameters ))
# pl.ylim(-2,2)
# pl.show()

class Interaction:
    def __init__(self, potential, cutoff, parameters):
        self.potential = potential
        self.cutoff = cutoff
        self.parameters = parameters


class Box:
    def __init__(self, lengths, corner):
        self.lengths = lengths
        self.corner = corner

        if lengths[0] == lengths[1] == lengths[2]:
            self.side = lengths[0]
            self.hside = 0.5 * self.side
            self.cubic = True
        else:
            self.cubic = False


class Simulation:
    def __init__(self, particles, box, interaction):
        self.r = particles
        self.box = box
        self.interaction = interaction


    def energy(self):
        tree = cKDTree(self.r, boxsize=self.box.lengths)
        distance = scipy.sparse.triu(tree.sparse_distance_matrix(tree, self.interaction.cutoff), k=0)
        distance.eliminate_zeros()
        dists = np.array(list(distance.todok().values()))
        self.current_energy = self.interaction.potential(dists, self.interaction.parameters).sum()
        return self.current_energy

    def energy_at(self, position, p):
        indices = np.arange(self.r.shape[0])
        dr = self.r[indices != p] - position
        dr[dr > self.box.hside] -= self.box.side
        dr[dr < -self.box.hside] += self.box.side

        norm_dr = np.linalg.norm(dr, axis=1)

        norm_dr = norm_dr[norm_dr < self.interaction.cutoff]

        u = self.interaction.potential(norm_dr, self.interaction.parameters).sum()

        return u


# start with one particle
r = np.array([
    [0, 0, 0]
])

r = ut.load('last_pos.dat.xyz')
sim = Simulation(r, Box([L, L, L], [0, 0, 0]), Interaction(twosteps, r3, parameters))
# insert particles
# r = moves.insert_hard_spheres(sim, N, r1, r3)

# ut.write_xyz("begin.xyz", sim.r)

move = moves.LocalMove(sim, delta, beta)

# x = np.arange(0,4,0.01)
# pl.plot(x, sim.interaction.potential(x,sim.interaction.parameters))
# pl.ylim(-2,2)
# pl.show()
for it in tqdm.tqdm(range(iterations)):

    N = sim.r.shape[0]
    for k in range(N):
        move.do()

    if it % 100 == 0:
        ut.write_xyz(f'tj/frame{it:06d}.xyz', sim.r)
