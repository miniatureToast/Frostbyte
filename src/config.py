import os

# define output directory
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# define export directory
EXPORT_DIR = os.path.join(OUTPUT_DIR, "frames")
os.makedirs(EXPORT_DIR, exist_ok=True)
# -------------------------------

# Time stepping
DT = 5e-3           # Step interval (sec)
SUBSTEPS = 40       # Num of calcs per step
STEPS_COUNT = 2250  # Total steps

# Environment
MPM_LOWER_BOUND = (-5.0, -0.3, -0.2) 
MPM_UPPER_BOUND = (5.0, 0.3, 1.5)
GRAVITY = (0.0, 0.0, -9.81)    
GRID_DENSITY = 70

# Snow Geometry
SNOW_POS = (0.0, 0.0, 0.25)
SNOW_SIZE = (1.0, 0.5, 0.2)

# Snow Material
SNOW_YOUNG_MODULUS = 1e4    # stiffness (lower is softer)
SNOW_POISSON_RATIO = 0.2    # packing ability (lower is looser)
SNOW_DENSITY = 50.0         # density in kg/m^3 (lower is fluffier)

# Robot
PLOW_POS = (-0.9, 0.0, 0.0)
PLOW_SIZE = (0.3, 0.5, 0.25)
PLOW_MASS = 20.0 # v3 original: 20.5          
PLOW_DENSITY = 1937.7
PLOW_FRICTION = 0.5

PLOW_VELOCITY = (0.3, 0.0, 0.0, 0.0, 0.0, 0.0)