import os
import xml.etree.ElementTree as ET 

import argparse

parser = argparse.ArgumentParser("Prepare a dynamo run with step potenial")

parser.add_argument('--density',default=0.85, type=float)
parser.add_argument('--thermostat',default=1.0,type=float)
args = parser.parse_args()


T = args.thermostat
density = args.density
print("Themrostat T", T, "density", density)
cmd = f'dynamod -m 16 -C 18 --zero-momentum -T {T}  -o start.xml --density {density}'

os.system(cmd)
tree = ET.parse('start.xml')
tree = tree.getroot()

discontinuities = [("1.5","1.0"),("1.0","1.0000000000000001e+300")]

for interaction in tree.findall('.//Interaction'):
    for c in interaction.findall('.//CaptureMap'):
        interaction.remove(c)
    for p in interaction.findall('.//Potential'):
        for s in p.findall('Step'):
            p.remove(s)
        child = ET.Element("Step")
        for d in  discontinuities:
            child.set('R',d[0])
            child.set('E',d[1])
            p.append(child)

with open(f'start.shoulder.xml', 'wb') as fw:
    fw.write(ET.tostring(tree))