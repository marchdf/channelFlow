#!/bin/bash
# Just run the paraview postprocessing script

set -ex

COMPILER=gcc
SPACK_ROOT=/projects/windFlowModeling/ExaWind/NaluSharedInstallationC/spack
SPACK=${SPACK_ROOT}/bin/spack

module purge
module use ${SPACK_ROOT}/share/spack/modules/$(${SPACK} arch)
module load openmpi-1.10.4-gcc-5.2.0-hlho57g
module load paraview

mpirun -np 24 pvbatch pp.py

