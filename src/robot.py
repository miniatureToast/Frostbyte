import genesis as gs
import trimesh
from . import config

def build_plow(scene):
    # Automatically find the lowest Z vertex of the .obj so it never spawns inside the floor
    mesh = trimesh.load(config.PLOW_FILE, force="mesh")
    min_z = float(mesh.bounds[0][2])
    
    # Shift spawn Z so the bottom of the mesh sits 2mm above Z = 0.0
    spawn_pos = (
        config.PLOW_POS[0],
        config.PLOW_POS[1],
        -min_z + 0.002,
    )
    if config.PLOW_FILE.endswith(".urdf"):
        robot_morph = gs.morphs.URDF(
            file=config.PLOW_FILE,
            pos=spawn_pos,
            euler=(0.0, 0.0, 90.0), # rotation fix
            scale=1.0,
            collision=True,
        )
    else:
        robot_morph = gs.morphs.Mesh(
            file=config.PLOW_FILE,
            pos=spawn_pos, 
            euler=(0.0, 0.0, 90.0), # rotation fix
            scale=1.0, 
            collision=True, 
        )

    plow = scene.add_entity(
        material=gs.materials.Rigid(
            rho=config.PLOW_DENSITY, 
            friction=config.PLOW_FRICTION
        ),
        morph = robot_morph,
        surface=gs.surfaces.Default(
            color=(0.5, 0.5, 0.55, 1.0)
        ),
    )
    return plow