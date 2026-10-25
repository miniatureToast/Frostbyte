import polyscope as ps
import polyscope.imgui as psim
import glob
import open3d as o3d 
import pandas as pd 
import numpy as np
import trimesh # <--- NEW IMPORT

ps.init()
ps.set_up_dir("z_up")

ps.set_automatically_center_zoom(False)  # Stops Polyscope from hijacking your zoom
ps.set_navigation_style("free")          # Keeps camera movement smooth and stable

snow_files = sorted(glob.glob("output/frames/snow_*.ply")) # or mpm_output_frames
plow_data = pd.read_csv("output/plow_positions.csv")

# Load the CAD mesh using Trimesh
mesh = trimesh.load("assets/frosty_v3_sim.obj", force='mesh')

# Register the properly sized CAD model into Polyscope
ps_robot = ps.register_surface_mesh("Robot", mesh.vertices, mesh.faces, color=(1.0, 0.5, 0.0))
ps_robot.set_edge_width(1.0)

frame_idx = 0
playing = False

def update_frame():
    global frame_idx
    if frame_idx >= len(snow_files):
        frame_idx = 0
        
    # 1. Update the Snow Point Cloud
    pcd = o3d.io.read_point_cloud(snow_files[frame_idx])
    ps.register_point_cloud("Snow", np.asarray(pcd.points), radius=0.005, color=(0.92, 0.96, 1.0))
    
    # 2. Update the CAD Model's Position
    # Grab the current X,Y,Z from the CSV
    current_pos = plow_data.iloc[frame_idx][["X", "Y", "Z"]].values
    
    # We update the internal transformation matrix to move the mesh!
    # (Since it was centered at 0,0,0 in Blender, adding the current_pos places it perfectly)
    transform = np.eye(4)
    transform[0:3, 3] = current_pos
    ps_robot.set_transform(transform)
    
def callback():
    global frame_idx, playing
    psim.Text(f"Frame: {frame_idx} / {len(snow_files)}")
    if psim.Button("Play/Pause"):
        playing = not playing
    if playing:
        update_frame()
        frame_idx += 1

ps.set_user_callback(callback)
update_frame() 
ps.show()