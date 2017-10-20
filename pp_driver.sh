#!/bin/bash
# Just run the paraview postprocessing script

set -ex

COMPILER=gcc
SPACK_ROOT=/projects/windFlowModeling/ExaWind/SharedSoftware/spack
SPACK=${SPACK_ROOT}/bin/spack

module purge
module use ${SPACK_ROOT}/share/spack/modules/$(${SPACK} arch)

module load $(${SPACK} module find -m tcl openmpi %${COMPILER})
module load $(${SPACK} module find -m tcl paraview %${COMPILER})

mpirun -np 24 pvbatch pp.py

