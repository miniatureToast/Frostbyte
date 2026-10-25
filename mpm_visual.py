import src.config as config
import polyscope as ps
import polyscope.imgui as psim
import glob
import open3d as o3d 
import pandas as pd 
import numpy as np
import trimesh

ps.init()
ps.set_up_dir("z_up")

# 1. Load file paths
snow_files = sorted(glob.glob("output/frames/snow_*.ply"))
plow_data = pd.read_csv("output/plow_positions.csv")
print(f"Found {len(snow_files)} snow frames!")

# 2. Load and register the Robot mesh ONCE
mesh = trimesh.load("assets/frosty_v3_sim.obj", force='mesh')
ps_robot = ps.register_surface_mesh("Robot", mesh.vertices, mesh.faces, color=(1.0, 0.5, 0.0))
ps_robot.set_edge_width(1.0)

# --- ANCHOR THE WORLD ORIGIN ---
# Register a tiny, invisible or subtle bounding box right where the snow starts (0,0,0).
# This forces Polyscope's bounding-box center to stay permanently locked at the origin, 
# preventing the floor grid from drifting when the robot moves!
anchor_box = trimesh.creation.box(extents=[0.01, 0.01, 0.01])
anchor_box.apply_translation([0.0, 0.0, 0.0])
ps_anchor = ps.register_surface_mesh("WorldAnchor", anchor_box.vertices, anchor_box.faces)
ps_anchor.set_transparency(0.0) # Completely invisible, purely acts as a spatial anchor!

# 3. Register the Snow Point Cloud ONCE using the first frame
initial_pcd = o3d.io.read_point_cloud(snow_files[0])
initial_points = np.asarray(initial_pcd.points)
ps_snow = ps.register_point_cloud("Snow", initial_points, color=(0.92, 0.96, 1.0))
ps_snow.set_radius(0.003, relative=False)  # Lock physical world size

frame_idx = 0
playing = False

def update_frame():
    global frame_idx
    if frame_idx >= len(snow_files):
        frame_idx = 0
    if frame_idx < 0:
        frame_idx = len(snow_files) - 1
        
    # --- UPDATE POSITIONS IN-PLACE (Stops grid shifting!) ---
    pcd = o3d.io.read_point_cloud(snow_files[frame_idx])
    ps_snow.update_point_positions(np.asarray(pcd.points))
    
    # Update Robot Position from CSV
    current_pos = plow_data.iloc[frame_idx][["X", "Y", "Z"]].values
    transform = np.eye(4)
    transform[0:3, 3] = current_pos
    ps_robot.set_transform(transform)

def callback():
    global frame_idx, playing
    
    save_interval = 5  
    sim_time = frame_idx * config.DT * save_interval
    
    psim.Text(f"Frame: {frame_idx} / {len(snow_files) - 1}")
    psim.Text(f"Time: {sim_time:.2f} seconds")
    psim.Separator()
    
    changed, new_val = psim.SliderInt("Scrubber", frame_idx, 0, len(snow_files) - 1)
    if changed:
        frame_idx = new_val
        update_frame()
    
    if psim.Button("Play/Pause"):
        playing = not playing
        
    if playing:
        update_frame()
        frame_idx += 1

ps.set_user_callback(callback)
update_frame() 

# --- ABSOLUTE CAMERA LOCK (Executed last) ---
ps.look_at(
    camera_location=(-0.0, -2.0, 1.2),  
    target=(0.0, 0.0, 0.2)             
)

ps.show()