import os

# define output directory
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# define export directory
EXPORT_DIR = os.path.join(OUTPUT_DIR, "frames")
os.makedirs(EXPORT_DIR, exist_ok=True)
# -------------------------------

# 1. Increase substeps for MPM stability
DT = 1e-2
SUBSTEPS = 25  
GRAVITY = (0.0, 0.0, -9.81)

MPM_LOWER_BOUND = (-5.0, -0.55, -0.2) 
MPM_UPPER_BOUND = (5.0, 0.55, 1.5)
GRID_DENSITY = 32

# Terrain & Snow Parameters
SNOW_YOUNG_MODULUS = 1e5    # Soft, packable snow
SNOW_POISSON_RATIO = 0.2
SNOW_DENSITY = 350.0

# Snow Bed Geometry
SNOW_POS = (0.0, 0.0, 0.12)
SNOW_SIZE = (2.0, 0.8, 0.20)

# Robot Payload Parameters
PLOW_POS = (-1.6, 0.0, 0.0)
PLOW_SIZE = (0.3, 0.5, 0.25)
PLOW_MASS = 20.5           
PLOW_FRICTION = 0.4
PLOW_VELOCITY = (0.5, 0.0, 0.0, 0.0, 0.0, 0.0)