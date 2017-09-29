Turbulent Channel Flow from the Workshop on High-Order CFD Methods
==================================================================

This presents large eddy simulation efforts of a turbulent channel
flow at :math:`Re_\tau = 550` using `Nalu
<https://github.com/NaluCFD/Nalu>`_ . The setup, grids, and
specifications are taken from the `Workshop on High-Order CFD Methods
<https://how5.cenaero.be/content/ws2-les-plane-channel-ret550>`_.

Simulation description
----------------------

The friction Reynolds number is kept constant through a forcing in the
:math:`x`-direction momentum equation. The forcing is imposed by a
pressure gradient and related to the friction Reynolds number:

.. math::

   Re_\tau = \frac{\delta u_\tau}{\nu}

   u_\tau = \sqrt{\frac{\tau_w}{\rho}}

   \frac{d p}{dx} = \frac{\tau_w}{\delta}

where :math:`\delta = 1` is the half height of the channel. The
computational domain is :math:`2\pi\delta \times 2 \delta \times \pi
\delta`. The initial condition is chosen to avoid long transient times
and is based on the Reichardt function:

.. math::

   u^+ = \frac{u}{u_\tau} = \frac{1}{\kappa} \ln(1+\kappa y^+) + \left( C - \frac{1}{\kappa} \ln(\kappa)\right) \left( 1 - e^{-\frac{y^+}{11}} - \frac{y^+}{11} e^{-\frac{y^+}{3}}\right)

where :math:`y^+=\frac{\Delta y}{y_\tau} = \frac{u_\tau y}{\nu}`,
:math:`\kappa = 0.4` is the Von Karman constant, and :math:`C` is an
integration constant. Sinusoidal perturbations of different
wavelenghts can be used to perturb the initial condition. The
simulations are run for at least :math:`40 t^+`. Statistics are
accumulated starting at :math:`20t^+` and are collected for at least
:math:`20t^+`. Temporal and spatial (wall-parallel directions)
averaged profiles in wall units for the following quantities are
computed and compared to reference data:

- time averaged velocity, :math:`\overline{u^+} = \frac{\overline{u}}{u_\tau}`

- velocity variances, :math:`(u')^+_{\text{rms}} = \frac{\sqrt{\overline{u' u'}}}{u_\tau}` (similarly for :math:`v` and :math:`w`)

- Velocity component temporal cross-correlations, :math:`-\overline{(u'v')^+} = \frac{\overline{u'v'}}{u^2_\tau}` (similarly for :math:`vw` and :math:`wu`)

The temporal evolution of the following quantities will also be provided:

- the integrated shear stress at top and bottom walls separately

- the mass flux through the inlet plane.


Using this repository
---------------------

A.  Generating the meshes

    1. Download the meshes from `Workshop on High-Order CFD Methods <https://how5.cenaero.be/content/ws2-les-plane-channel-ret550>`_
    #. Open the `.geo` file in Gmsh and apply the 3D mesh. Save the mesh and export it to VTK format as well (Make sure to check "Save All"). Edit the `.geo` file and uncomment the different `nl` lines for the different mesh resolutions.
    #. Convert the VTK mesh to ExodusII format using `vtk2exo.py`
    #. Use Cubit to add sidesets to the meshes by using `add_sidesets.jou` (you might have to edit it a bit to get what you want)

B. Running

   .. code-block:: bash

		   $ mpiexec -np 1 ./naluX -i channelFlow.i

C. Post-processing

   .. code-block:: bash

		   $ ./plot_validation.py

