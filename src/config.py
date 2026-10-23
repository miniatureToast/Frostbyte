# System Physics
TIME_STEP = 1e-3
GRAVITY = -9.81
SETTLE_TIME = 0.4        # Seconds to let snow pack before applying horizontal plow force

# Terrain Trough Dimensions (Matches the rectangular channel in the video)
TROUGH_LENGTH_X = 3.0    # meters (along X plowing direction)
TROUGH_WIDTH_Y = 1.2     # meters (narrower Y width concentrates particles in the path)
WALL_HEIGHT = 0.4        # Containment wall height

# Granular Snow Parameters (High-Cohesion Packed Snow)
SNOW_RADIUS = 0.028
SNOW_DENSITY = 350
SNOW_LAYERS = 5

SNOW_FRICTION = 0.9          # Sliding friction
SNOW_ROLLING_FRICTION = 0.015 # CRITICAL: Stops spheres from rolling like marbles
SNOW_SPINNING_FRICTION = 0.015 # CRITICAL: Locks particle clumps together in shear
SNOW_RESTITUTION = 0.0       # Zero bounce
SNOW_COHESION = 1.5          # Normal adhesion force (N) to hold vertical rut walls
SNOW_YOUNG_MODULUS = 2e5     # Soft, compressible snow stiffness (Pa)
SNOW_POISSON_RATIO = 0.3

SPAWN_JITTER = 0.002
SPAWN_SPACING_MULT = 2.15    # Tighter initial spacing for faster packing

# Test Box / Plow Payload Parameters
TEST_MASS = 250              # Tuned so it sinks realistically without bottoming out instantly
TEST_DIMS = (0.5, 0.6, 0.4)  # (X-length, Y-width, Z-height)
DROP_HEIGHT = 0.45           # Spawns just above the snow surface
PUSH_FORCE = 1800            # Horizontal bulldozing force (N)