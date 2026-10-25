import trimesh
import numpy as np

# Load your perfectly centered mesh
mesh = trimesh.load("assets/frosty_v3_sim.obj", force='mesh')

# Spin it 90 degrees around the Z-axis permanently
# (If it ends up facing exactly away from the snow, change 90 to -90)
rot_z = trimesh.transformations.rotation_matrix(np.radians(90), [0, 0, 1])
mesh.apply_transform(rot_z)

# Overwrite the file with the perfectly aligned version
mesh.export("assets/frosty_v3_sim.obj")
print("Mesh permanently rotated to face forward and saved!")