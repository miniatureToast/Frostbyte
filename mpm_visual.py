import src.config as config
import polyscope as ps
import polyscope.imgui as psim
import glob
import open3d as o3d 
import pandas as pd 
import numpy as np
import trimesh # <--- NEW IMPORT

ps.init()
ps.set_up_dir("z_up")

snow_files = sorted(glob.glob("output/frames/snow_*.ply")) # or mpm_output_frames
plow_data = pd.read_csv("output/plow_positions.csv")

# Load the CAD mesh using Trimesh
mesh = trimesh.load("assets/frosty_v3_sim.obj", force='mesh')

# Register the properly sized CAD model into Polyscope
ps_robot = ps.register_surface_mesh("Robot", mesh.vertices, mesh.faces, color=(1.0, 0.5, 0.0))
ps_robot.set_edge_width(1.0)

# --- ABSOLUTE CAMERA LOCK ---
# ps.look_at(camera_location, target_look_at)
ps.look_at(
    camera_location=(-2.5, -2.0, 1.2),  # Where the camera sits in XYZ space
    target=(-0.5, 0.0, 0.2)             # What point the camera stares at (near the snow/robot)
)

frame_idx = 0
playing = False

def update_frame():
    global frame_idx
    if frame_idx >= len(snow_files):
        frame_idx = 0
    if frame_idx < 0:
        frame_idx = len(snow_files) - 1
        
    # 1. Load Snow Point Cloud
    pcd = o3d.io.read_point_cloud(snow_files[frame_idx])
    
    # Register point cloud
    ps_snow = ps.register_point_cloud("Snow", np.asarray(pcd.points), color=(0.92, 0.96, 1.0))
    
    # --> FORCE FIXED WORLD RADIUS & STOP AUTO-SCALING <--
    ps_snow.set_radius(0.003, relative=False)  # 0.003 meters absolute world size
    
    # Force a smaller, consistent radius so they don't look bloated
    #ps.register_point_cloud("Snow", np.asarray(pcd.points), radius=0.003, color=(0.92, 0.96, 1.0))
    
    # 2. Update Robot Position from CSV
    current_pos = plow_data.iloc[frame_idx][["X", "Y", "Z"]].values
    transform = np.eye(4)
    transform[0:3, 3] = current_pos
    ps_robot.set_transform(transform)

    # --> NEW: Force Polyscope to ONLY auto-center on the very first frame, 
    # preventing it from zooming or shifting during playback/scrubbing! <--
    if frame_idx == 0:
        ps.reset_camera_to_home_view()

def callback():
    global frame_idx, playing
    
    # --- REAL-TIME SIMULATION CLOCK ---
    # Calculate exact physical time elapsed (assuming you saved every 5 frames, 
    # adjust the multiplier if your save frequency in mpm_sim.py is different)
    save_interval = 5  
    sim_time = frame_idx * config.DT * save_interval
    
    # Render live stats in the Polyscope UI window
    psim.Text(f"Frame: {frame_idx} / {len(snow_files) - 1}")
    psim.Text(f"Time: {sim_time:.2f} seconds")
    psim.Separator()
    
    # --- INTERACTIVE TIMELINE SLIDER ---
    changed, new_val = psim.SliderInt("Scrubber", frame_idx, 0, len(snow_files) - 1)
    if changed:
        frame_idx = new_val
        update_frame()
    
    # Play / Pause button
    if psim.Button("Play/Pause"):
        playing = not playing
        
    if playing:
        update_frame()
        frame_idx += 1

ps.set_user_callback(callback)
update_frame() 
ps.show()