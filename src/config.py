# System Physics
TIME_STEP = 5e-3  
GRAVITY = -9.81

### Grandular Snow 
# Particle parameters
SNOW_FRICTION = 0.9      
SNOW_RESTITUTION = 0.0   
SNOW_COHESION = 1.0      # Reduced from 50.0 so they don't implode
SNOW_RADIUS = 0.03       
SNOW_DENSITY = 300       
GRID_LIMIT = 25          
SNOW_LAYERS = 5          # NEW: Thicker snow depth
SNOW_YOUNG_MODULUS = 2e5 
SPAWN_JITTER = 0.002

# --- NEW: Spacing multiplier ---
SPAWN_SPACING_MULT = 2.5 # Forces a physical gap so they fall into each other       

# Material compression
SNOW_YOUNG_MODULUS = 2e5 # Default is 2e7 (steel). 2e5 makes it softer and compressible.
SPAWN_JITTER = 0.002     # Tiny jitter to break symmetry without overlapping

# Test box parameters
TEST_MASS = 500
TEST_DIMS = (1, 1, 1)
DROP_HEIGHT = 0.8        # Lowered so it starts right above the snow
PUSH_FORCE = 3500        # NEW: Newtons of force to push the box sideways