#!/usr/bin/env python2

from vtk import vtkUnstructuredGridReader
from vtk import vtkExodusIIWriter

# Setup
iname = 'channel_structured_0.vtk'
oname = 'channel_structured_0.exo'

# Read VTK mesh
reader = vtkUnstructuredGridReader()
reader.SetFileName(iname)
reader.ReadAllVectorsOn()
reader.ReadAllScalarsOn()
reader.Update()
data = reader.GetOutput()

# Write out to Exodus
writer = vtkExodusIIWriter()
writer.WriteAllTimeStepsOn()
writer.WriteOutGlobalNodeIdArrayOn()
writer.SetFileName(oname)
writer.SetInputData(data)
writer.Write()
