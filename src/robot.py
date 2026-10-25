import genesis as gs
from . import config

def build_plow(scene):
    plow = scene.add_entity(
        material=gs.materials.Rigid(
            rho=config.PLOW_MASS, 
            friction=config.PLOW_FRICTION
        ),
        # --> Make sure this 'morph=' section is intact! <--
        morph=gs.morphs.Mesh(
            file="assets/frosty_v3_sim.obj",
            pos=config.PLOW_POS, 
            scale=1.0, 
            collision=True, 
        ),
        surface=gs.surfaces.Default(
            color=(0.5, 0.5, 0.55, 1.0)
        ),
    )
    return plow