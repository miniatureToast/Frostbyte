# Summary
This is the repository for team **Frostbyte**, which consists (four?) undergraduate students Pranav T, Rohit V, Yuanrui Z (??), and Gary F (me!). 

Currently this repo only contains our physics simulator for testing our v2 snowplow robot, which is still in development as of October 2026.
# Physics Simulator
Our physics sim runs on the **Genesis World** engine. Since our robot functions in a snow-based environment, the sim uses Genesis' mpm module to simulate and visualize snow behavior.
## Instructions (mac ONLY)
1) Download the latest `.zip`  release code.
	- not currently available rn lmao, I would just clone it
2) Create the **conda** environment.
	- Open project root in terminal
	- Install dependency from homebrew: `brew install libusb`
	- Enter `conda env create -f environment.yml`
	- If it doesn't work somehow, install the dependencies manually with `pip install <dependency>`
		1) *genesis-world*: the physics engine
		2) *open3d*: the baker for saving sim frames
		3) *polyscope*: the 3D visualizer
		4) *tqdm*: a progress bar loader hehe
		5) *pandas*: a `.csv` parser
3) Run and Visualize the sim.
	1) Execute `python mpm_sim.py` to bake the physics data
	2) `ppython mpm_visual.py` to open visualizer

# Random Stuff
So far the physics sim is solo-dev by Gary (me). Future plans might include operator code for our custom PCB later. 