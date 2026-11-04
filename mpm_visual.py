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

# ---> NEW: AUTOMATIC COM SYNC <---
# Compare Frame 0's physical COM to the config spawn origin.
# This finds the exact offset for ANY plow geometry automatically!
frame_0_pos = plow_data.iloc[0][["X", "Y", "Z"]].values
spawn_pos = np.array(config.PLOW_POS)
auto_com_offset = frame_0_pos - spawn_pos

# 2. Load and register the Robot mesh ONCE
mesh = trimesh.load(config.PLOW_FILE, force='mesh')
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
ps_snow.set_radius(0.005, relative=False)

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
    points = np.asarray(pcd.points)

    # nn_dists = np.asarray(pcd.compute_nearest_neighbor_distance())
    
    # # Invert the distance so smaller distance = higher pressure.
    # # We use 0.02 (the resting distance for GRID_DENSITY=50) to normalize it!
    # # Loose snow = ~1.0. Packed snow = 2.0 to 4.0+.
    # packing_pressure = 0.02 / (nn_dists + 1e-6) 
    
    # # Apply the heatmap to the snow in Polyscope!
    # # 'jet' cmap maps loose snow to Blue, and high-stress packed snow to Red
    # ps_snow.add_scalar_quantity(
    #     "Packing Pressure", 
    #     packing_pressure, 
    #     enabled=True, 
    #     cmap='jet', 
    #     vminmax=(0.8, 2.5) # Locks the color scale so it doesn't flicker (tune as needed!)
    # )

    # Update Robot Position from CSV
    current_pos = plow_data.iloc[frame_idx][["X", "Y", "Z"]].values
    transform = np.eye(4)

    #TEMPORAORY
    # NEW: Apply a 90-degree rotation around the Z-axis!
    # (If it faces away from the snow, just swap the 1.0 and -1.0)
    transform[0:3, 0:3] = np.array([
        [ 0.0, -1.0,  0.0],
        [ 1.0,  0.0,  0.0],
        [ 0.0,  0.0,  1.0]
    ])

    transform[0:3, 3] = current_pos - auto_com_offset
    ps_robot.set_transform(transform)

def callback():
    global frame_idx, playing
    
    sim_time = frame_idx * config.DT * config.FRAME_INTERVAL
    
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

# Camera view
ps.look_at(
    camera_location=(1.7, -1.7, 1.2),  
    target=(0.0, 0.0, 0.2)             
)

ps.show()