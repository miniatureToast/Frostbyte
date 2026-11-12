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
ps.set_front_dir("x_front")

snow_files = sorted(glob.glob("output/frames/snow_*.ply"))
plow_data = pd.read_csv("output/plow_positions.csv")
print(f"Found {len(snow_files)} snow frames!")

frame_0_pos = plow_data.iloc[0][["X", "Y", "Z"]].values
spawn_pos = np.array(config.PLOW_POS)

# load obj mesh
mesh = trimesh.load(config.PLOW_FILE, force='mesh')
ps_robot = ps.register_surface_mesh("Robot", mesh.vertices, mesh.faces, color=(1.0, 0.5, 0.0))
ps_robot.set_edge_width(1.0)

anchor_box = trimesh.creation.box(extents=[0.01, 0.01, 0.01])
anchor_box.apply_translation([0.0, 0.0, 0.0])
ps_anchor = ps.register_surface_mesh("WorldAnchor", anchor_box.vertices, anchor_box.faces)
ps_anchor.set_transparency(0.0) # Completely invisible, purely acts as a spatial anchor!

# register snow point-cloud
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
        
    pcd = o3d.io.read_point_cloud(snow_files[frame_idx])
    ps_snow.update_point_positions(np.asarray(pcd.points))
    points = np.asarray(pcd.points)

    # update obj pos from baked frames
    current_pos = plow_data.iloc[frame_idx][["X", "Y", "Z"]].values
    transform = np.eye(4)

    # TEMPORAORY
    # apply 90-deg rotation
    transform[0:3, 0:3] = np.array([
        [ 0.0, -1.0,  0.0],
        [ 1.0,  0.0,  0.0],
        [ 0.0,  0.0,  1.0]
    ])

    transform[0:3, 3] = current_pos
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

# camera view
ps.look_at(
    camera_location=(1.7, -1.7, 1.2),  
    target=(0.0, 0.0, 0.2)             
)

ps.show()