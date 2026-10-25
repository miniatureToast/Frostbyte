import os

# define output directory
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# define export directory
EXPORT_DIR = os.path.join(OUTPUT_DIR, "frames")
os.makedirs(EXPORT_DIR, exist_ok=True)
# -------------------------------

# --- TEMPORAL SCALING (Real-World Proportions) ---
DT = 5e-3        # Smaller base time step for finer calculations
SUBSTEPS = 40    # High substeps so gravity and collisions have time to resolve smoothly
STEPS_COUNT = 4500
GRAVITY = (0.0, 0.0, -9.81)

MPM_LOWER_BOUND = (-5.0, -2.0, -0.2) 
MPM_UPPER_BOUND = (5.0, 2.0, 1.5)
GRID_DENSITY = 70

# Snow Bed Geometry
SNOW_POS = (0.0, 0.0, 0.2)
SNOW_SIZE = (1.0, 0.5, 0.1)

# Terrain & Snow Parameters
SNOW_YOUNG_MODULUS = 5e4    # Soft, packable snow
SNOW_POISSON_RATIO = 0.2
SNOW_DENSITY = 250.0

# Robot Payload Parameters
PLOW_POS = (-0.9, 0.0, 0.0)
PLOW_SIZE = (0.3, 0.5, 0.25)
PLOW_MASS = 45.0 # v3 original: 20.5          
PLOW_FRICTION = 0.5

PLOW_VELOCITY = (0.3, 0.0, 0.0, 0.0, 0.0, 0.0)