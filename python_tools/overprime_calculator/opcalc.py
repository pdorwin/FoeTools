# obcalc.py
import subprocess
import sys
import os

def main():
    here = os.path.dirname(os.path.abspath(__file__))
    gui = os.path.join(here, "opcalc_gui.py")

    # Start detached (Windows + Linux)
    if sys.platform.startswith("win"):
        subprocess.Popen(
            [sys.executable, gui],
            creationflags=subprocess.DETACHED_PROCESS
        )
    else:
        subprocess.Popen(
            [sys.executable, gui],
            start_new_session=True
        )

if __name__ == "__main__":
    main()
