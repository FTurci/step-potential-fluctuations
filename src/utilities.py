import numpy as np

def write_xyz(fname, r,types=None):
	with open(fname, 'w') as fw:
		fw.write('%d\nParticles\n'%r.shape[0])

		if types==None:
			for i,p in enumerate(r):
				fw.write(f'A {p[0]} {p[1]} {p[2]}\n')

def load(fname):
	with open(fname) as fr:
		return np.loadtxt(fname, skiprows=2, usecols= [1,2,3])

		