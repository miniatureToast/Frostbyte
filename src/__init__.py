import os

# SCMTerrain bugged rn on mac, ONLY USE 1 THREAD
# os.environ["OMP_NUM_THREADS"] = "1"

# Granular phys not bugged
os.environ["OMP_NUM_THREADS"] = "8"