import genesis as gs
from . import config

def build_plow(scene):
    """Adds the rigid plow test box to the scene."""
    
    plow = scene.add_entity(
        material=gs.materials.Rigid(
            rho=config.PLOW_MASS, 
            friction=config.PLOW_FRICTION
        ),
        morph=gs.morphs.Box(
            pos=config.PLOW_POS,
            size=config.PLOW_SIZE,
        ),
        surface=gs.surfaces.Default(
            color=(0.2, 0.2, 0.25, 1.0)
        ),
    )
    
    return plow