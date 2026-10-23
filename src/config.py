import os

# --- NEW DIRECTORY STRUCTURE ---
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Export Settings for Visualization
EXPORT_DIR = os.path.join(OUTPUT_DIR, "frames")
os.makedirs(EXPORT_DIR, exist_ok=True)
# -------------------------------

# 1. Increase substeps for MPM stability (This stops math explosions)
DT = 1e-2
SUBSTEPS = 25  
GRAVITY = (0.0, 0.0, -9.81)

# 2. Expand the left MPM boundary so we have room to move the plow back
MPM_LOWER_BOUND = (-1.6, -0.6, -0.15) 
MPM_UPPER_BOUND = (1.3, 0.6, 0.5)      
GRID_DENSITY = 32

# Terrain & Snow Parameters (MPM Elasto-Plastic)
SNOW_YOUNG_MODULUS = 1e5    # Soft, packable snow
SNOW_POISSON_RATIO = 0.2
SNOW_DENSITY = 350.0

# Snow Bed Geometry
SNOW_POS = (0.0, 0.0, 0.12)
SNOW_SIZE = (2.0, 0.8, 0.20)

# Plow Payload Parameters
PLOW_POS = (-1.25, 0.0, 0.15) # Left face is now at -1.4, right face is at -1.1 (safely away from the -1.0 snow)
PLOW_SIZE = (0.3, 0.5, 0.25)
PLOW_MASS = 400.0           
PLOW_FRICTION = 0.4
PLOW_VELOCITY = [0.6, 0.0, 0.0, 0.0, 0.0, 0.0]  # Move right at 0.6 m/s