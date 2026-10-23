import os
import site
import sys

def link_binaries(chrono_build_dir="../chrono/build"):
    build_path = os.path.abspath(os.path.join(os.path.dirname(__file__), chrono_build_dir, "bin"))
    if not os.path.isdir(build_path):
        print(f"Error: Could not locate Chrono bin folder at {build_path}")
        sys.exit(1)

    site_packages = site.getsitepackages()[0]
    pth_file = os.path.join(site_packages, "pychrono_native.pth")
    with open(pth_file, "w") as f:
        f.write(build_path + "\n")

    print(f"Successfully linked native Chrono binaries to:\n{pth_file}")

if __name__ == "__main__":
    link_binaries() 