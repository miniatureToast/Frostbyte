import genesis as gs
from . import config

def build_environment(scene):
    """Adds the solid ground and MPM snow bed to the scene."""
    
    # 1. Solid Ground Plane
    scene.add_entity(
        morph=gs.morphs.Plane(),
        material=gs.materials.Rigid(friction=0.9),
    )

    # 2. Elasto-Plastic MPM Snow Bed
    snow_bed = scene.add_entity(
        material=gs.materials.MPM.Snow(
            E=config.SNOW_YOUNG_MODULUS,             
            nu=config.SNOW_POISSON_RATIO,            
            rho=config.SNOW_DENSITY,         
        ),
        morph=gs.morphs.Box(
            pos=config.SNOW_POS,
            size=config.SNOW_SIZE,
        ),
        surface=gs.surfaces.Default(
            color=(0.92, 0.96, 1.0, 1.0),
            vis_mode="particle",
        ),
    )
    
    return snow_bed