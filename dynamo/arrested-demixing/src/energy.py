from dynamoutils import io
import glob
from stringato import extract_floats as ef
import natsort
import matplotlib.pyplot as pl

import numpy as np

files = natsort.natsorted(glob.glob("Snapshot.output.*.xml.bz2"))

u = np.array(list(map(io.read_uconfig,files)))
t = np.array(list(map(io.read_time,files)))

N = io.read_quantity(files[0],'ParticleCount')
print(u)
pl.plot(t,u/N)
pl.ylabel("U/N")
pl.xlabel("$t/t_0$")
pl.show()