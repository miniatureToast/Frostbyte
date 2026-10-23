import pychrono as chrono
from . import config

def build_ground(sys):
    """Creates the solid underlying floor plane."""
    ground_mat = chrono.ChContactMaterialSMC()
    
    # NEW: Soften the ground and kill its bounce so particles can settle
    ground_mat.SetYoungModulus(config.SNOW_YOUNG_MODULUS)
    ground_mat.SetRestitution(config.SNOW_RESTITUTION)
    ground_mat.SetFriction(config.SNOW_FRICTION)
    
    # Ground top face sits exactly at Z = 0
    ground = chrono.ChBodyEasyBox(20, 20, 1, 1000, True, True, ground_mat)
    ground.SetPos(chrono.ChVector3d(0, 0, -0.5))
    ground.SetFixed(True)
    sys.Add(ground)
    return ground

import pychrono as chrono
from . import config
import random

def build_granular_snow(sys):
    """Spawns the grid of physical snow spheres in multiple layers."""
    snow_mat = chrono.ChContactMaterialSMC()
    snow_mat.SetFriction(config.SNOW_FRICTION)
    snow_mat.SetRestitution(config.SNOW_RESTITUTION)
    snow_mat.SetAdhesion(config.SNOW_COHESION) 
    
    # NEW: Soften the material so it absorbs impacts rather than exploding
    snow_mat.SetYoungModulus(config.SNOW_YOUNG_MODULUS)
    snow_mat.SetPoissonRatio(0.3)

    num_layers = 3 
    
    # Calculate spacing to ensure an absolute zero-overlap air gap
    spacing = config.SNOW_RADIUS * config.SPAWN_SPACING_MULT 

    # Use the new config parameter for thickness
    for z in range(config.SNOW_LAYERS):
        # Spawn them higher up so they drop into a pile
        z_offset = (config.SNOW_RADIUS * 2) + (z * spacing) 
        
        for x in range(-config.GRID_LIMIT, config.GRID_LIMIT):
            for y in range(-config.GRID_LIMIT, config.GRID_LIMIT):
                # Use the heavily reduced jitter
                jitter_x = random.uniform(-config.SPAWN_JITTER, config.SPAWN_JITTER)
                jitter_y = random.uniform(-config.SPAWN_JITTER, config.SPAWN_JITTER)

                snow = chrono.ChBodyEasySphere(
                    config.SNOW_RADIUS, 
                    config.SNOW_DENSITY, 
                    True, True, snow_mat
                )
                
                snow.SetPos(chrono.ChVector3d(
                    (x * spacing) + jitter_x, 
                    (y * spacing) + jitter_y, 
                    z_offset
                ))
                sys.Add(snow)