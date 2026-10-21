import os
os.environ["OMP_NUM_THREADS"] = "1" # single-thread so hashmap doesnt tweak

import pychrono as chrono
import pychrono.vehicle as veh
import pychrono.irrlicht as chronoirr
import math

# Set default data path to load built-in visualizer assets (lights, fonts)
chrono.SetChronoDataPath(chrono.GetChronoDataPath())

# 1. Initialize the Multibody Physics System
sys = chrono.ChSystemSMC()
sys.SetCollisionSystemType(chrono.ChCollisionSystem.Type_BULLET)
sys.SetGravitationalAcceleration(chrono.ChVector3d(0, 0, -9.81))

# 2. Solid Ground Plane (Stable floor)
ground_mat = chrono.ChContactMaterialSMC()
ground = chrono.ChBodyEasyBox(20, 20, 1, 1000, True, True, ground_mat)
ground.SetPos(chrono.ChVector3d(0, 0, -0.5))
ground.SetFixed(True)
sys.Add(ground)

# 3. Granular Snow Particles (Stable on ARM64)
snow_mat = chrono.ChContactMaterialSMC()
snow_mat.SetFriction(0.6)
snow_mat.SetRestitution(0.0) # Snow deadens impact

# Spawn a patch of 400 physical snow spheres
for x in range(-10, 10):
    for y in range(-10, 10):
        snow = chrono.ChBodyEasySphere(0.05, 300, True, True, snow_mat)
        snow.SetPos(chrono.ChVector3d(x * 0.11, y * 0.11, 0.05))
        sys.Add(snow)

# 4. Test Box Drop
box_mat = chrono.ChContactMaterialSMC()
test_box = chrono.ChBodyEasyBox(1, 1, 1, 500, True, True, box_mat)
test_box.SetPos(chrono.ChVector3d(0, 0, 3))
sys.Add(test_box)

# 3. Set up the Irrlicht 3D Visualizer
vis = chronoirr.ChVisualSystemIrrlicht()
vis.AttachSystem(sys)
vis.SetWindowSize(1280, 720)
vis.SetWindowTitle("Snow Bot - SCM Sandbox")
vis.Initialize()
vis.AddCamera(chrono.ChVector3d(0, -6, 3), chrono.ChVector3d(0, 0, 0))
vis.AddTypicalLights()

# 4. Execute the Physics Loop
time_step = 2e-3
while vis.Run():
    vis.BeginScene()
    vis.Render()
    vis.EndScene()
    
    # Advance the simulation by one timestep
    sys.DoStepDynamics(time_step)