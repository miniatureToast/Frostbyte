import genesis as gs
from . import config

# init sim environment and objects
def build_environment(scene):
    """Adds the solid ground and MPM snow bed to the scene."""
    
    # solid ground plane
    scene.add_entity(
        morph=gs.morphs.Plane(),
        material=gs.materials.Rigid(friction=config.TERRAIN_FRICTION),
    )

    # mpm snow point-cloud
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