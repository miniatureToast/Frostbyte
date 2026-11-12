import src
import genesis as gs
from src import config, terrain, robot
import csv
import time
import os
import open3d as o3d
import glob
from tqdm import tqdm

print("Clearing previous frames...")
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

initial_vel = [0.0] * 6  # [X, Y, Z, Roll, Pitch, Yaw]
plow.set_dofs_velocity(initial_vel)

# baked frames export directory + telemetry
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

    locked_pos = plow.get_pos().clone()
    locked_quat = plow.get_quat().clone()

    for step in tqdm(range(config.STEPS_COUNT), desc="Baking Frames", unit="step"):

        # force y/z position and orientation
        curr_pos = plow.get_pos().clone()
        curr_pos[1] = locked_pos[1]  # Lock Y
        curr_pos[2] = locked_pos[2]  # Lock Z
        plow.set_pos(curr_pos)
        plow.set_quat(locked_quat)   # Lock Roll, Pitch, Yaw orientation

        # force x-velocity only
        current_vel = plow.get_dofs_velocity()
        current_vel[0] = config.PLOW_VELOCITY if step > 50 else 0.0
        current_vel[1:] = 0.0
        plow.set_dofs_velocity(current_vel)
            
        scene.step()
        
        # export frames
        if step % config.FRAME_INTERVAL == 0:
            # save snow particles
            snow_path = os.path.join(config.EXPORT_DIR, f"snow_{frame_idx:04d}.ply")
            points = snow_bed.get_particles_pos().cpu().numpy()
            pcd = o3d.geometry.PointCloud()
            pcd.points = o3d.utility.Vector3dVector(points)
            o3d.io.write_point_cloud(snow_path, pcd)
            
            # save plow pos
            plow_pos = plow.get_pos().cpu().numpy()
            pos_writer.writerow([frame_idx, plow_pos[0], plow_pos[1], plow_pos[2]])
            
            frame_idx += 1
        
        # log telemetry (unused rn)
        if step % 10 == 0:
            forces = -plow.get_dofs_force().cpu().numpy()
            sim_time = step * config.DT
            telemetry_writer.writerow([
                step, f"{sim_time:.3f}",
                f"{forces[0]:.2f}", f"{forces[1]:.2f}", f"{forces[2]:.2f}",
                f"{forces[3]:.2f}", f"{forces[4]:.2f}", f"{forces[5]:.2f}"
            ])

print(f"\nSimulation Baked in {time.time() - start_time:.1f} seconds.")