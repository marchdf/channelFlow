#
# Run this script on NERSC Edison with something like:
#    start_pvbatch.sh 4 4 00:10:00 default debug `pwd`/pp.py
#


# ----------------------------------------------------------------
# imports
# ----------------------------------------------------------------
# import the simple module from the paraview
from paraview.simple import *
# disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

import os
import glob
import shutil
import numpy as np

# ----------------------------------------------------------------
# setup
# ----------------------------------------------------------------

# Get file names
workdir = os.path.dirname(os.path.abspath(__file__))
fdir = os.path.abspath(os.path.join(workdir, 'coarse'))
rdir = os.path.join(fdir, 'results')
pattern = '*.e.*'
fnames = sorted(glob.glob(os.path.join(rdir, pattern)))
oname = os.path.join(fdir, 'mdot.dat')

# ----------------------------------------------------------------
# setup the data processing pipelines
# ----------------------------------------------------------------

# create a new 'ExodusIIReader'
exoreader = ExodusIIReader(FileName=fnames)
exoreader.PointVariables = ['velocity_']
exoreader.SideSetArrayStatus = ['inlet']
exoreader.ElementBlocks = []

# get time
times = exoreader.TimestepValues

# mesh quality
mesh = MeshQuality(Input=exoreader)
mesh.TriangleQualityMeasure = 'Area'
mesh.QuadQualityMeasure = 'Area'

# create a new 'Integrate Variables'
integral = IntegrateVariables(Input=mesh)

# show data in view
integrateVariables1Display = Show(integral)

# get animation scene
animationScene1 = GetAnimationScene()
animationScene1.GoToFirst()

# loop on each time and write to file
mdot = np.zeros((len(times), 5))
for i, t in enumerate(times):

    area = integral.CellData.GetArray(0).GetRange(0)[0]
    u = integral.PointData.GetArray(2).GetRange(0)[0] / area
    v = integral.PointData.GetArray(2).GetRange(1)[0] / area
    w = integral.PointData.GetArray(2).GetRange(2)[0] / area

    mdot[i, :] = np.array([t, area, u, v, w])

    animationScene1.AnimationTime = t

np.savetxt(oname,
           mdot,
           delimiter=',',
           header="time,area,uavg,vavg,wavg",
           comments='')
