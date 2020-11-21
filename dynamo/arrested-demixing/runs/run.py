import os
import xml.etree.ElementTree as ET 




T = 1.0
density = 0.85
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

with open('start2.xml', 'wb') as fw:
    fw.write(ET.tostring(tree))