import os

# Output directory
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Export directory
EXPORT_DIR = os.path.join(OUTPUT_DIR, "frames")
os.makedirs(EXPORT_DIR, exist_ok=True)

# --- SCENE ---
# Steps
DT = 5e-3           # Step interval (sec)
SUBSTEPS = 40       # Num of calcs per step
STEPS_COUNT = 1500  # Total steps
FRAME_INTERVAL = 5  # N steps per frame

# Environment
MPM_LOWER_BOUND = (-1.5, -1.2, -0.1) 
MPM_UPPER_BOUND = (2.0, 1.2, 0.8)
GRAVITY = (0.0, 0.0, -9.81)    
GRID_DENSITY = 40

TERRAIN_FRICTION = 5.0

# --- SNOW  ---
SNOW_POS = (0.0, 0.0, 0.065)
SNOW_SIZE = (1.0, 1.5, 0.12) # width should be 2x-3x of plow width

# STIFFNESS (lower is softer)
# 1e3 (powder) to 3e4 (compact) to 5e5 (icy)
SNOW_YOUNG_MODULUS = 3e3    

# PACKING ability (lower is looser)
# 0.1 (powder) to 0.2 (compact) to 0.35 (icy)
SNOW_POISSON_RATIO = 0.2

# DENSITY in kg/m^3 (lower is fluffier)
# 50.0 (powder) to 200.0 (compact) to 400.0 (icy)
SNOW_DENSITY = 300.0

# --- ROBOT --- 
PLOW_FILE = "assets/plow3.obj"

PLOW_POS = (-0.9, 0.0, 0.001)
PLOW_SIZE = (0.3, 0.5, 0.25)
PLOW_MASS = 20.0 # v3 original: 20.5          
PLOW_DENSITY = 1937.7 # v3: 1937.7
PLOW_FRICTION = 0.1 

#PLOW_FORCE = n/a
PLOW_VELOCITY = 0.3 # xdirection m/s