# -*- mode: yaml -*-
Simulations:
  - name: sim1
    time_integrator: ti_1
    optimizer: opt1

linear_solvers:

  - name: solve_scalar
    type: tpetra
    method: gmres
    preconditioner: sgs
    tolerance: 1e-8
    max_iterations: 75
    kspace: 75
    output_level: 0

  - name: solve_cont
    type: tpetra
    method: gmres
    preconditioner: muelu
    tolerance: 1e-8
    max_iterations: 75
    kspace: 75
    output_level: 0
    muelu_xml_file_name: ../muelu.xml
    recompute_preconditioner: no

realms:

  - name: realm_1
    mesh: ../mesh/channel_structured_0.exo
    use_edges: no
    automatic_decomposition_type: rcb

    time_step_control:
     target_courant: 10.0
     time_step_change_factor: 1.2

    equation_systems:
      name: theEqSys
      max_iterations: 3

      solver_system_specification:
        velocity: solve_scalar
        pressure: solve_cont
        turbulent_ke: solve_scalar

      systems:

        - LowMachEOM:
            name: myLowMach
            max_iterations: 1
            convergence_tolerance: 1.0e-5

        - TurbKineticEnergy:
            name: myTke
            max_iterations: 3
            convergence_tolerance: 1.0e-2


    initial_conditions:
      - constant: ic_1
        target_name: [Unspecified-2-HEX]
        value:
          pressure: 0
          velocity: [34.6,0.0,0.0]
          turbulent_ke: 0.00108

    material_properties:
      target_name: [Unspecified-2-HEX]
      specifications:
        - name: density
          type: constant
          value: 1.185
        - name: viscosity
          type: constant
          value: 1.8398e-5

    boundary_conditions:

    - wall_boundary_condition: bc_wall
      target_name: bottomwall
      wall_user_data:
        velocity: [0,0,0]
        turbulent_ke: 0.0
        use_wall_function: yes

    - wall_boundary_condition: bc_wall
      target_name: topwall
      wall_user_data:
        velocity: [0,0,0]
        turbulent_ke: 0.0
        use_wall_function: yes

    - inflow_boundary_condition: bc_inflow
      target_name: inlet
      inflow_user_data:
        velocity: [34.6,0.0,0.0]
        turbulent_ke: 0.00108

    - open_boundary_condition: bc_open
      target_name: outlet
      open_user_data:
        velocity: [0,0,0]
        pressure: 0.0
        turbulent_ke: 0.00108

    - periodic_boundary_condition: bc_front_back
      target_name: [front, back]
      periodic_user_data:
        search_tolerance: 0.0001

    solution_options:
      name: myOptions
      turbulence_model: ksgs

      options:
        - hybrid_factor:
            velocity: 1.0
            turbulent_ke: 1.0

        - alpha_upw:
            velocity: 1.0

        - limiter:
            pressure: no
            velocity: no
            turbulent_ke: no

        - projected_nodal_gradient:
            velocity: element
            pressure: element
            turbulent_ke: element


    turbulence_averaging:
      time_filter_interval: 100000.0


    post_processing:

    - type: surface
      physics: surface_force_and_moment
      output_file_name: results/channelFlow.dat
      frequency: 100
      parameters: [0,0]
      target_name: bottomwall

    output:
      output_data_base_name: results/channelFlow.e
      output_frequency: 100
      output_node_set: no
      output_variables:
       - velocity
       - pressure
       - pressure_force
       - tau_wall
       - turbulent_ke

    restart:
      restart_data_base_name: restart/channelFlow.rst
      output_frequency: 5000

Time_Integrators:
  - StandardTimeIntegrator:
      name: ti_1
      start_time: 0
      time_step: 1.0e-10
      termination_time: 1000
      time_stepping_type: adaptive
      time_step_count: 0

      realms:
        - realm_1
