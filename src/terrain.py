import random
import pychrono as chrono
from . import config

def create_snow_material():
    """Creates the shared SMC material for snow-snow and snow-wall interactions."""
    mat = chrono.ChContactMaterialSMC()
    mat.SetYoungModulus(config.SNOW_YOUNG_MODULUS)
    mat.SetPoissonRatio(config.SNOW_POISSON_RATIO)
    mat.SetFriction(config.SNOW_FRICTION)
    mat.SetRollingFriction(config.SNOW_ROLLING_FRICTION)
    mat.SetSpinningFriction(config.SNOW_SPINNING_FRICTION)
    mat.SetRestitution(config.SNOW_RESTITUTION)
    mat.SetAdhesion(config.SNOW_COHESION)
    return mat

def build_ground(sys):
    """Creates a solid floor with lateral containment walls like the video testbed."""
    ground_mat = create_snow_material()
    # Ground shouldn't glue particles permanently, just provide high friction
    ground_mat.SetAdhesion(0.0)

    # 1. Base Floor
    floor = chrono.ChBodyEasyBox(
        config.TROUGH_LENGTH_X + 0.4, 
        config.TROUGH_WIDTH_Y + 0.4, 
        0.2, 1000, True, True, ground_mat
    )
    floor.SetPos(chrono.ChVector3d(0, 0, -0.1))
    floor.SetFixed(True)
    sys.Add(floor)

    # 2. Lateral Containment Walls (Front, Back, Left, Right)
    wall_thickness = 0.1
    half_x = config.TROUGH_LENGTH_X / 2.0 + (wall_thickness / 2.0)
    half_y = config.TROUGH_WIDTH_Y / 2.0 + (wall_thickness / 2.0)
    wall_z = config.WALL_HEIGHT / 2.0

    # Side walls (along X)
    for y_sign in [-1, 1]:
        side_wall = chrono.ChBodyEasyBox(
            config.TROUGH_LENGTH_X + 0.2, wall_thickness, config.WALL_HEIGHT,
            1000, False, True, ground_mat  # False = invisible collision wall for clean camera view
        )
        side_wall.SetPos(chrono.ChVector3d(0, y_sign * half_y, wall_z))
        side_wall.SetFixed(True)
        sys.Add(side_wall)

    # End walls (along Y)
    for x_sign in [-1, 1]:
        end_wall = chrono.ChBodyEasyBox(
            wall_thickness, config.TROUGH_WIDTH_Y, config.WALL_HEIGHT,
            1000, False, True, ground_mat
        )
        end_wall.SetPos(chrono.ChVector3d(x_sign * half_x, 0, wall_z))
        end_wall.SetFixed(True)
        sys.Add(end_wall)

    return floor

def build_granular_snow(sys):
    """Spawns a high-cohesion granular snowbed inside the containment trough."""
    snow_mat = create_snow_material()
    spacing = config.SNOW_RADIUS * config.SPAWN_SPACING_MULT

    # Calculate grid counts to fill the rectangular trough
    nx = int((config.TROUGH_LENGTH_X / 2.0 - config.SNOW_RADIUS * 2) / spacing)
    ny = int((config.TROUGH_WIDTH_Y / 2.0 - config.SNOW_RADIUS * 2) / spacing)

    snow_color = chrono.ChVisualMaterial()
    snow_color.SetDiffuseColor(chrono.ChColor(0.92, 0.95, 1.0))

    count = 0
    for z in range(config.SNOW_LAYERS):
        z_offset = (config.SNOW_RADIUS * 1.5) + (z * spacing)
        # Offset alternating layers by half-spacing (hexagonal close-packing)
        layer_shift = (spacing * 0.5) if (z % 2 == 1) else 0.0

        for ix in range(-nx, nx):
            for iy in range(-ny, ny):
                jitter_x = random.uniform(-config.SPAWN_JITTER, config.SPAWN_JITTER)
                jitter_y = random.uniform(-config.SPAWN_JITTER, config.SPAWN_JITTER)

                snow = chrono.ChBodyEasySphere(
                    config.SNOW_RADIUS,
                    config.SNOW_DENSITY,
                    True, True, snow_mat
                )
                snow.SetPos(chrono.ChVector3d(
                    (ix * spacing) + layer_shift + jitter_x,
                    (iy * spacing) + layer_shift + jitter_y,
                    z_offset
                ))
                snow.GetVisualShape(0).SetMaterial(0, snow_color)
                sys.Add(snow)
                count += 1

    print(f"[Frostbyte] Spawned {count} cohesive snow particles.")