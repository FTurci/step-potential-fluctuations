import numpy as np
from scipy.spatial import cKDTree
import scipy

def insert_hard_spheres(sim,N,sigma,cutoff):
	r = sim.r
	L = sim.box.lengths[0]
	print("[Inserting particles...]")
	while r.shape[0]<N:
		
		# pick a point at random in a CUBIC box
		point = np.random.uniform(0,L,(1,3))
		r= np.append(r,point, axis=0)
		# print(r)
		# construct tree
		tree = cKDTree(r,boxsize=[L,L,L]);
		distance = scipy.sparse.triu(tree.sparse_distance_matrix(tree,cutoff), k=0)
		distance.eliminate_zeros()
		
		dists = np.array(list(distance.todok().values()))

		if len(dists)>0 and np.any(dists<sigma):
			r = r[:-1]
	sim.r =r 


class LocalMove():
	def __init__(self,sim,delta, beta):
		self.delta = delta
		self.beta = beta
		self.sim = sim

	def do(self):
		L = self.sim.box.lengths[0]
		
		# pick a particles
		# print(self.sim.r.shape)
		p = np.random.randint(0,self.sim.r.shape[0])

		old_e = self.sim.energy_at(self.sim.r[p],p)
		new_r = self.sim.r[p]+np.random.uniform(-self.delta, self.delta, (1,3))
		new_r[new_r>L]-=L
		new_r[new_r<0]+=L
		new_e = self.sim.energy_at(new_r,p)
		delta_e  = new_e-old_e
		if np.random.uniform(0,1)< np.exp(-self.beta*delta_e):
			self.sim.r[p] = new_r
		else:
			pass


def mc_sweep(sim, kinds, frequencies, ):
	N = sim.r.shape[0]
	for k in range(N):
		for kind in kinds:
			if kind == 'local':
				local_move()

