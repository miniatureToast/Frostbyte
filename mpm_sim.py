import src
import genesis as gs
from src import config, terrain, robot
import csv
import time
import os
import open3d as o3d
import glob
from tqdm import tqdm

print("Clearing old simulation frames...")
old_frames = glob.glob(os.path.join(config.EXPORT_DIR, "*"))
for f in old_frames:
    os.remove(f)

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
    show_viewer=False,
)

snow_bed = terrain.build_environment(scene)
plow = robot.build_plow(scene)
scene.build()

print("Starting Headless Plowing with Frame Baking...")
start_time = time.time()
frame_idx = 0 

# export location for baked outputs
telemetry_path = os.path.join(config.OUTPUT_DIR, "plow_telemetry.csv")
positions_path = os.path.join(config.OUTPUT_DIR, "plow_positions.csv")

with open(telemetry_path, mode="w", newline="") as telemetry_file, \
     open(positions_path, mode="w", newline="") as pos_file:
     
    telemetry_writer = csv.writer(telemetry_file)
    telemetry_writer.writerow([
        "Step", "Time (s)", 
        "Force_X (N)", "Force_Y (N)", "Force_Z (N)", 
        "Torque_Roll (Nm)", "Torque_Pitch (Nm)", "Torque_Yaw (Nm)"
    ])
    
    pos_writer = csv.writer(pos_file)
    pos_writer.writerow(["Frame", "X", "Y", "Z"])
    
    for step in tqdm(range(config.STEPS_COUNT), desc="Baking Frames", unit="step"):
        
        if step > 50:
            plow.set_dofs_velocity(config.PLOW_VELOCITY)
            
        scene.step()
        
        # Export Visual Frames
        if step % config.FRAME_INTERVAL == 0:
            # 1. Save Snow Points
            snow_path = os.path.join(config.EXPORT_DIR, f"snow_{frame_idx:04d}.ply")
            points = snow_bed.get_particles_pos().cpu().numpy()
            pcd = o3d.geometry.PointCloud()
            pcd.points = o3d.utility.Vector3dVector(points)
            o3d.io.write_point_cloud(snow_path, pcd)
            
            # 2. Save Plow Position
            # get_pos() returns an array like [X, Y, Z]
            plow_pos = plow.get_pos().cpu().numpy()
            pos_writer.writerow([frame_idx, plow_pos[0], plow_pos[1], plow_pos[2]])
            
            frame_idx += 1
        
        # Log Full 6-DoF Telemetry
        if step % 10 == 0:
            # Invert forces to represent the resistance load applied BY the snow ON the plow
            forces = -plow.get_dofs_force().cpu().numpy()
            sim_time = step * config.DT
            telemetry_writer.writerow([
                step, f"{sim_time:.3f}",
                f"{forces[0]:.2f}", f"{forces[1]:.2f}", f"{forces[2]:.2f}",
                f"{forces[3]:.2f}", f"{forces[4]:.2f}", f"{forces[5]:.2f}"
            ])
            
print(f"\nSimulation Baked in {time.time() - start_time:.1f} seconds.")