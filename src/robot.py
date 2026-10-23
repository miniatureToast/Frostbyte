import pychrono as chrono
from . import config
from .terrain import create_snow_material

def build_test_box(sys):
    """Spawns the test plow box at the start of the trough."""
    box_mat = create_snow_material()
    box_mat.SetAdhesion(0.0) # Prevent snow from permanently gluing to the top of the box
    
    w, l, h = config.TEST_DIMS
    test_box = chrono.ChBodyEasyBox(w, l, h, config.TEST_MASS, True, True, box_mat)
    
    # Spawn near the negative-X end of the trough
    start_x = -(config.TROUGH_LENGTH_X / 2.0) + (w / 2.0) + 0.15
    test_box.SetPos(chrono.ChVector3d(start_x, 0, config.DROP_HEIGHT))
    sys.Add(test_box)
    
    # Create horizontal thruster (starts at 0 N until snow settles)
    plow_force = chrono.ChForce()
    test_box.AddForce(plow_force)
    plow_force.SetMode(chrono.ChForce.FORCE)
    plow_force.SetAlign(chrono.ChForce.WORLD_DIR)
    plow_force.SetDir(chrono.ChVector3d(1, 0, 0))
    plow_force.SetMforce(0.0)
    
    return test_box, plow_force