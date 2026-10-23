import polyscope as ps
import polyscope.imgui as psim
import glob
import open3d as o3d 
import pandas as pd # pip install pandas (easier CSV reading)
import numpy as np

ps.init()
ps.set_up_dir("z_up") 

# ---> UPDATE THESE TWO PATHS <---
snow_files = sorted(glob.glob("output/frames/snow_*.ply"))
plow_data = pd.read_csv("output/plow_positions.csv")

PLOW_SIZE = np.array([0.3, 0.5, 0.25])

frame_idx = 0
playing = False

def update_frame():
    global frame_idx
    if frame_idx >= len(snow_files):
        frame_idx = 0
        
    # Load Snow Point Cloud
    pcd = o3d.io.read_point_cloud(snow_files[frame_idx])
    ps.register_point_cloud("Snow", np.asarray(pcd.points), radius=0.005, color=(0.92, 0.96, 1.0))
    
    # Draw the Plow using the logged position
    current_pos = plow_data.iloc[frame_idx][["X", "Y", "Z"]].values
    
    # To draw a box in Polyscope, we define its 8 corners relative to its center
    half_extents = PLOW_SIZE / 2.0
    min_bounds = current_pos - half_extents
    max_bounds = current_pos + half_extents
    
    # Define the 8 corners of the bounding box
    nodes = np.array([
        [min_bounds[0], min_bounds[1], min_bounds[2]],
        [max_bounds[0], min_bounds[1], min_bounds[2]],
        [max_bounds[0], max_bounds[1], min_bounds[2]],
        [min_bounds[0], max_bounds[1], min_bounds[2]],
        [min_bounds[0], min_bounds[1], max_bounds[2]],
        [max_bounds[0], min_bounds[1], max_bounds[2]],
        [max_bounds[0], max_bounds[1], max_bounds[2]],
        [min_bounds[0], max_bounds[1], max_bounds[2]]
    ])
    
    # Define the 12 edges connecting the corners
    edges = np.array([
        [0, 1], [1, 2], [2, 3], [3, 0], # Bottom face edges
        [4, 5], [5, 6], [6, 7], [7, 4], # Top face edges
        [0, 4], [1, 5], [2, 6], [3, 7]  # Vertical edges connecting top to bottom
    ])
    
    # Register it as a wireframe curve network so we can see the snow pushing against it
    ps.register_curve_network("Plow Wireframe", nodes, edges, radius=0.003, color=(1.0, 0.5, 0.0))
    
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