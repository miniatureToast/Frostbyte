import pychrono as chrono
from . import config

import pychrono as chrono
from . import config

def build_test_box(sys):
    """Drops a test payload and pushes it sideways to simulate plowing."""
    box_mat = chrono.ChContactMaterialSMC()
    w, l, h = config.TEST_DIMS
    
    test_box = chrono.ChBodyEasyBox(w, l, h, config.TEST_MASS, True, True, box_mat)
    
    # Spawn at the left edge (-1.5 on X axis) and lower the drop height
    test_box.SetPos(chrono.ChVector3d(-1.5, 0, config.DROP_HEIGHT))
    sys.Add(test_box)
    
    # Add a continuous horizontal force to simulate a bulldozer driving forward
    plow_force = chrono.ChForce()
    test_box.AddForce(plow_force)
    plow_force.SetMode(chrono.ChForce.FORCE)
    plow_force.SetAlign(chrono.ChForce.WORLD_DIR) # Always push strictly along global X
    plow_force.SetDir(chrono.ChVector3d(1, 0, 0)) # Positive X direction
    plow_force.SetMforce(config.PUSH_FORCE)       # Apply the thrust we set in config
    
    return test_box