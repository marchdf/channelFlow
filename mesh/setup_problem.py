#!/usr/bin/env python3
"""Setup the channel flow problem
"""

# ========================================================================
#
# Imports
#
# ========================================================================
import os
import yaml
import numpy as np
import subprocess as sp

# ========================================================================
#
# Setup
#
# ========================================================================
delta = 1
L = [2 * np.pi * delta,
     2 * delta,
     np.pi * delta]
N = [128, 96, 64]

polynomial_order = 1.
Re_tau = 550
viscosity = 0.0000157

dbname = 'channel_coarse'
msh_dbname = dbname + ".exo"
ic_dbname = dbname + "_ic.exo"

mpibin = '/Users/mhenryde/spack/opt/spack/darwin-elcapitan-x86_64/gcc-6.3.0/openmpi-1.10.3-ljq6fsplvbw4qjiia4ho7xy4lcghu44o/bin/mpiexec'
abl_mesh = '/Users/mhenryde/wind/NaluWindUtils/build/src/mesh/abl_mesh'
nalu_preprocess = '/Users/mhenryde/wind/NaluWindUtils/build/src/preprocessing/nalu_preprocess'

# ========================================================================
#
# Generate new mesh and IC files
#
# ========================================================================

# Load the skeleton data
msh_iname = "mesh.yaml"
msh_inp = yaml.load(open(msh_iname, 'r'))
msh_data = msh_inp['nalu_abl_mesh']

ic_iname = "ic.yaml"
ic_inp = yaml.load(open(ic_iname, 'r'))
ic_data = ic_inp['nalu_preprocess']

# New yaml mesh file
msh_oname = "msh_tmp.yaml"
msh_data['output_db'] = msh_dbname
vertices = msh_data['vertices']
vertices[1][0] = L[0]
vertices[1][1] = L[1]
vertices[1][2] = L[2]
msh_data['mesh_dimensions'] = N
y_spacing = msh_data['y_spacing']
y_spacing['stretching_factor'] = 1.2**(polynomial_order / 2.0)

with open(msh_oname, 'w') as of:
    yaml.dump(msh_inp, of, default_flow_style=False)

# New yaml IC file
ic_oname = "ic_tmp.yaml"
ic_data['input_db'] = msh_dbname
ic_data['output_db'] = ic_dbname
task = ic_data['init_channel_fields']
velocity = task['velocity']
velocity['Re_tau'] = Re_tau
velocity['viscosity'] = viscosity

with open(ic_oname, 'w') as of:
    yaml.dump(ic_inp, of, default_flow_style=False)

# ========================================================================
#
# Run the utilities
#
# ========================================================================

proc = sp.Popen(mpibin + ' -np 1 ' + abl_mesh + ' -i ' + msh_oname,
                shell=True,
                stderr=sp.PIPE)
err = proc.communicate()
errcode = proc.returncode

proc = sp.Popen(mpibin + ' -np 1 ' + nalu_preprocess + ' -i ' + ic_oname,
                shell=True,
                stderr=sp.PIPE)
err = proc.communicate()
errcode = proc.returncode

# ========================================================================
#
# Clean up
#
# ========================================================================
os.remove(msh_oname)
os.remove(ic_oname)
