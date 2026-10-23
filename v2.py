import src  # Runs __init__.py (sets OMP_NUM_THREADS)
import pychrono as chrono
import pychrono.irrlicht as chronoirr
from src import config, terrain, robot

chrono.SetChronoDataPath(chrono.GetChronoDataPath())

# Shrink collision envelopes for tight granular packing
chrono.ChCollisionModel.SetDefaultSuggestedEnvelope(0.002)
chrono.ChCollisionModel.SetDefaultSuggestedMargin(0.001)

# 1. Initialize System with Hertzian Granular Contact Model
sys = chrono.ChSystemSMC()
sys.SetNumThreads(8)
sys.SetCollisionSystemType(chrono.ChCollisionSystem.Type_BULLET)
sys.SetContactForceModel(chrono.ChSystemSMC.Hertz)
sys.SetTangentialDisplacementModel(chrono.ChSystemSMC.MultiStep)
sys.UseMaterialProperties(True)
sys.SetGravitationalAcceleration(chrono.ChVector3d(0, 0, config.GRAVITY))

# 2. Build the Trough & Snow World
terrain.build_ground(sys)
terrain.build_granular_snow(sys)
test_payload, plow_force = robot.build_test_box(sys)

# 3. Setup the Visualizer
vis = chronoirr.ChVisualSystemIrrlicht()
vis.AttachSystem(sys)
vis.SetWindowSize(1280, 720)
vis.SetWindowTitle("Frostbyte - High-Cohesion DEM Snow Trough")
vis.Initialize()
vis.AddCamera(chrono.ChVector3d(0, -2.5, 1.2), chrono.ChVector3d(0, 0, 0.1))
vis.AddTypicalLights()

# 4. Execute the Physics Loop
while vis.Run():
    vis.BeginScene()
    vis.Render()
    vis.EndScene()
    
    # Engage horizontal plow thrust after snow settles
    if sys.GetChTime() >= config.SETTLE_TIME:
        plow_force.SetMforce(config.PUSH_FORCE)
        
    sys.DoStepDynamics(config.TIME_STEP)