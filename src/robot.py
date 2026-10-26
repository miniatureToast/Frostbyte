import genesis as gs
from . import config

def build_plow(scene):
    if config.PLOW_FILE.endswith(".urdf"):
        robot_morph = gs.morphs.URDF(
            file=config.PLOW_FILE,
            pos=config.PLOW_POS,
            scale=1.0,
            collision=True,
        )
    else:
        robot_morph = gs.morphs.Mesh(
            file=config.PLOW_FILE,
            pos=config.PLOW_POS, 
            scale=1.0, 
            collision=True, 
        )

    plow = scene.add_entity(
        material=gs.materials.Rigid(
            rho=config.PLOW_DENSITY, 
            friction=config.PLOW_FRICTION
        ),
        # --> Make sure this 'morph=' section is intact! <--
        morph=robot_morph,
        surface=gs.surfaces.Default(
            color=(0.5, 0.5, 0.55, 1.0)
        ),
    )
    return plow