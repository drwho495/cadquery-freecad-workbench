from CQGui.display import show_object

# Register the show_object function as a global function
globals()['show_object'] = show_object

# Make sure the CadQuery packages are installed
try:
    import cadquery
except ImportError:
    import os
    import sys
    import subprocess
    os.environ.pop('CONDA_PREFIX', None)
    os.environ.pop('CONDA_PREFIX_1', None)
    subprocess.run(["python", "-m", "pip", "install", "--upgrade", "--force-reinstall", "cadquery==2.5.1"], capture_output=True)
    subprocess.run(["python", "-m", "pip", "install", "--upgrade", "--force-reinstall", "cadquery_ocp==7.7.2"], capture_output=True)
