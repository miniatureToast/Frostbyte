import src
import pychrono as chrono
import pychrono.irrlicht as chronoirr

from src import config, terrain, robot

chrono.ChCollisionModel.SetDefaultSuggestedEnvelope(0.002)
chrono.ChCollisionModel.SetDefaultSuggestedMargin(0.001)

# Initialize
sys = chrono.ChSystemSMC()
sys.SetNumThreads(8) # should match num threads in __init__.py
sys.SetCollisionSystemType(chrono.ChCollisionSystem.Type_BULLET)
sys.SetGravitationalAcceleration(chrono.ChVector3d(0, 0, config.GRAVITY))

# 2. Build the Simulation World
terrain.build_ground(sys)
terrain.build_granular_snow(sys)
test_payload = robot.build_test_box(sys)

# 3. Setup the Visualizer
vis = chronoirr.ChVisualSystemIrrlicht()
vis.AttachSystem(sys)
vis.SetWindowSize(1280, 720)
vis.SetWindowTitle("Frostbyte - Modular Granular Sandbox")
vis.Initialize()
vis.AddCamera(chrono.ChVector3d(0, -6, 3), chrono.ChVector3d(0, 0, 0))
vis.AddTypicalLights()

# 4. Execute the Physics Loop
while vis.Run():
    vis.BeginScene()
    vis.Render()
    vis.EndScene()
    
    sys.DoStepDynamics(config.TIME_STEP)