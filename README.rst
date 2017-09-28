Channel Flow from the high order CFD workshop
=============================================


Using this repository
---------------------

A.  Generating the meshes

    1. Download the meshes from the High Order CFD Workshop `<https://how5.cenaero.be/content/ws2-les-plane-channel-ret550>`_
    #. Open the `.geo` file in Gmsh and apply the 3D mesh. Save the mesh and export it to VTK format as well (Make sure to check "Save All"). Edit the `.geo` file and uncomment the different `nl` lines for the different mesh resolutions.
    #. Convert the VTK mesh to ExodusII format using `vtk2exo.py`
    #. Use Cubit to add sidesets to the meshes by using `add_sidesets.jou` (you might have to edit it a bit to get what you want)

B. Running

   .. code-block:: bash

		   $ mpiexec -np 1 ./naluX -i channelFlow.i

C. Post-processing

   .. code-block:: bash

		   $ ./plot_validation.py

