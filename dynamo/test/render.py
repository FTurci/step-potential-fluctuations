import math
from ovito.vis import *
import ovito									
from ovito.io import *
from ovito.modifiers import *	
import sys

node=import_file(sys.argv[1])	#all frames are extracted
    
node.add_to_scene()

vis_element = node.source.data.particles.vis

vis_element.radius = ParticlesVis
vp = Viewport()
vp.type = Viewport.Type.Perspective
print(vp.camera_pos, vp.camera_dir)
vp.camera_pos = (0,0, -50)

# vp.camera_dir = (0,0,0)
# vp.fov = math.radians(60.0)

vp.render_image(size=(800,600), filename="figure.png", background=(1,1,1),renderer=TachyonRenderer())


