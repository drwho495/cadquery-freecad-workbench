from CQGui.display import show_object

# Register the show_object function as a global function
globals()['show_object'] = show_object

# Make sure the CadQuery packages are installed
try:
    import cadquery
except ImportError:
    import sys
    import subprocess
    subprocess.run(["python", "-m", "pip", "install", "--upgrade", "cadquery==2.5.1"], capture_output=False)
    subprocess.run(["python", "-m", "pip", "install", "--upgrade", "cadquery_ocp==7.7.2"], capture_output=False)
