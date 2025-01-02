from CQGui.display import show_object

# Register the show_object function as a global function
globals()['show_object'] = show_object

# Make sure the CadQuery packages are installed
try:
    import cadquery
except ImportError:
    print("CadQuery is not installed. Installing now...")

    import os
    import sys
    import subprocess
    subprocess.run(["python", "-m", "pip", "install", "--upgrade", "cadquery==2.5.1"], capture_output=True)
    subprocess.run(["python", "-m", "pip", "install", "--upgrade", "cadquery-ocp==7.7.2"], capture_output=True)
    subprocess.run(["python", "-m", "pip", "install", "--upgrade", "ezdxf"], capture_output=True)
    subprocess.run(["python", "-m", "pip", "install", "--upgrade", "multimethod>=1.11,<2.0"], capture_output=True)
    subprocess.run(["python", "-m", "pip", "install", "--upgrade", "nlopt>=2.9.0,<3.0"], capture_output=True)
    subprocess.run(["python", "-m", "pip", "install", "--upgrade", "typish"], capture_output=True)
    subprocess.run(["python", "-m", "pip", "install", "--upgrade", "casadi"], capture_output=True)
    subprocess.run(["python", "-m", "pip", "install", "--upgrade", "path"], capture_output=True)

    print("CadQuery has been installed. Please restart FreeCAD.")
