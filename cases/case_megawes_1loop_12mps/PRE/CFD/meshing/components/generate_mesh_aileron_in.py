'''
generate_section_3Dmesh.py
author: Thomas Haas
date: 22.09.2023
description: Generate files for blockMesh utility
'''

# Imports
from mshGen.meshGeneration.mesh_class import Mesh
from matplotlib import pyplot as plt
import os

# ---------------------- Initialization ---------------------- #
path_cwd = os.getcwd()
plt.close("all")

# ---------------------- User settings ---------------------- #
'''
User settings
'''

# Case name:
airfoil_name = "Mrev-v2_aileron"
wing_name = "AILERON_IN"

# Path mshGen/meshGeneration
path_mshGen = "/cfdfile1/data/fm/niels/awesim/software/mshGen/meshGeneration"

# Airfoil file:
filename1 = path_cwd + "/airfoils/Mrev-v2_aileron.txt"

# Wing file:
filename2 = path_cwd + "/wings/MegAWES_aileron_in.txt"

# Output folder for default files:
foldername1 = path_mshGen + "/default_files"

# Output folder for BlockMesh files:
foldername2 = path_cwd + "/output_files"

# Case dimension (2D or 3D):
dim = "3D"

# Mesh origin (Center of gravity):
COG = [0.179,0,0]

# Mesh parameters:
slice_locations = [0,3.535,3.885]
layer_resolution = [60,10]
layer_grading =  [1,1]
layer_aileron = None
mesh_scale = 1.5
mesh_level = "COARSE"   # Mesh refinement level (Choose from: "COARSE")
skip_layer = 1 #not skiping if ARTIFICIOUS = False

# Flags
WRITE=True
PRINT=True
PLOT=False
DEFAULT=False # NOTE: Airfoil default files are tuned for mesh_scale == 5.

# optional flags to splt surfaces, used to match surface for FSI
SPLIT = True
ARTIFICIOUS = False

# Create inputs of Mesh instance
casename = [airfoil_name+"_"+dim+"_"+wing_name, airfoil_name, wing_name]
files = [filename1, filename2, foldername1, foldername2]
params = [dim, COG, slice_locations, layer_resolution, layer_grading, layer_aileron, mesh_scale, mesh_level,skip_layer]
flags = [WRITE, PRINT, PLOT, DEFAULT,SPLIT,ARTIFICIOUS]

# ---------------------- Create OpenFOAM mesh ---------------------- #
'''
Create OpenFOAM mesh
'''

# Create mesh
mesh = Mesh(casename, files, params, flags)

# Build mesh
mesh.initialize_mesh()                                              # Initialize mesh
mesh.generate_default()                                             # Generate mesh.default
mesh.generate_vertices()                                            # Generate mesh.vertices
mesh.generate_blocks()                                              # Generate mesh.blocks
mesh.generate_edges()                                               # Generate mesh.edges
mesh.generate_interfaces()                                          # Generate mesh.interfaces
mesh.generate_boundaries()                                          # Generate mesh.boundaries
if PLOT:
    plt.show()

# ---------------------- END ---------------------- #
