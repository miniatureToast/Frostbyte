import src
import genesis as gs
from src import config, terrain, robot
import csv
import time
import os
import open3d as o3d
from tqdm import tqdm

scene = gs.Scene(
    sim_options=gs.options.SimOptions(
        dt=config.DT,
        substeps=config.SUBSTEPS,
        gravity=config.GRAVITY,
    ),
    mpm_options=gs.options.MPMOptions(
        lower_bound=config.MPM_LOWER_BOUND,
        upper_bound=config.MPM_UPPER_BOUND,
        grid_density=config.GRID_DENSITY,
    ),
    show_viewer=False, # Keep headless for max speed
)

snow_bed = terrain.build_environment(scene)
plow = robot.build_plow(scene)
scene.build()

# ... (previous code) ...
print("Starting Headless Plowing with Frame Baking...")
start_time = time.time()
frame_idx = 0 

# ---> UPDATE THESE TWO PATHS <---
telemetry_path = os.path.join(config.OUTPUT_DIR, "plow_telemetry.csv")
positions_path = os.path.join(config.OUTPUT_DIR, "plow_positions.csv")

with open(telemetry_path, mode="w", newline="") as telemetry_file, \
     open(positions_path, mode="w", newline="") as pos_file:
     
    telemetry_writer = csv.writer(telemetry_file)
    # ... (the rest of the script remains exactly the same)
    telemetry_writer.writerow(["Step", "Time (s)", "Plow Resistance Force X (N)"])
    
    pos_writer = csv.writer(pos_file)
    pos_writer.writerow(["Frame", "X", "Y", "Z"])
    
    for step in tqdm(range(1500), desc="Baking Frames", unit="step"):
        
        if step > 50:
            plow.set_dofs_velocity(config.PLOW_VELOCITY)
            
        scene.step()
        
        # Export Visual Frames
        if step % 5 == 0:
            # 1. Save Snow Points (This part still works perfectly)
            snow_path = os.path.join(config.EXPORT_DIR, f"snow_{frame_idx:04d}.ply")
            points = snow_bed.get_particles_pos().cpu().numpy()
            pcd = o3d.geometry.PointCloud()
            pcd.points = o3d.utility.Vector3dVector(points)
            o3d.io.write_point_cloud(snow_path, pcd)
            
            # 2. Save Plow Position (Replacing the broken export_mesh)
            # get_pos() returns an array like [X, Y, Z]
            plow_pos = plow.get_pos().cpu().numpy()
            pos_writer.writerow([frame_idx, plow_pos[0], plow_pos[1], plow_pos[2]])
            
            frame_idx += 1
        
        # Log Telemetry
        if step % 10 == 0:
            resistance_force = -plow.get_dofs_force()[0].item() 
            sim_time = step * config.DT
            telemetry_writer.writerow([step, f"{sim_time:.3f}", f"{resistance_force:.2f}"])

print(f"\nSimulation Baked in {time.time() - start_time:.1f} seconds.")