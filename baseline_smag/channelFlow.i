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
    tolerance: 1e-5
    max_iterations: 75
    kspace: 75
    output_level: 0

  - name: solve_cont
    type: tpetra
    method: gmres
    preconditioner: muelu
    tolerance: 1e-5
    max_iterations: 75
    kspace: 75
    output_level: 0
    muelu_xml_file_name: ../muelu.xml
    recompute_preconditioner: no

realms:

  - name: realm_1
    mesh: ../mesh/channel_baseline_ic.exo
    use_edges: no
    automatic_decomposition_type: rcb
    support_inconsistent_multi_state_restart: yes

    time_step_control:
     target_courant: 1.0
     time_step_change_factor: 1.2

    equation_systems:
      name: theEqSys
      max_iterations: 3

      solver_system_specification:
        velocity: solve_scalar
        pressure: solve_cont

      systems:

        - LowMachEOM:
            name: myLowMach
            max_iterations: 1
            convergence_tolerance: 1.0e-5

    initial_conditions:
      - constant: ic_1
        target_name: [interior]
        value:
          pressure: 0
          velocity: [0.0,0.0,0.0]

    material_properties:
      target_name: [interior]
      specifications:
        - name: density
          type: constant
          value: 1.177
        - name: viscosity
          type: constant
          value: 1.846e-5

    boundary_conditions:

    - wall_boundary_condition: bc_bottomwall
      target_name: bottomwall
      wall_user_data:
        velocity: [0,0,0]
        use_wall_function: no

    - wall_boundary_condition: bc_topwall
      target_name: topwall
      wall_user_data:
        velocity: [0,0,0]
        use_wall_function: no

    - periodic_boundary_condition: bc_inlet_outlet
      target_name: [inlet, outlet]
      periodic_user_data:
        search_tolerance: 0.0001

    - periodic_boundary_condition: bc_front_back
      target_name: [front, back]
      periodic_user_data:
        search_tolerance: 0.0001

    solution_options:
      name: myOptions
      turbulence_model: smagorinsky

      options:
        - hybrid_factor:
            velocity: 0.0

        - alpha:
            velocity: 0.0

        - limiter:
            pressure: no
            velocity: no

        - projected_nodal_gradient:
            velocity: element
            pressure: element

        - input_variables_from_file:
            velocity: velocity

        - source_terms:
            momentum: body_force

        - source_term_parameters:
            momentum: [0.00008775, 0.0, 0.0]

    post_processing:

    - type: surface
      physics: surface_force_and_moment
      output_file_name: bottomwall.dat
      frequency: 100
      parameters: [0,0]
      target_name: [bottomwall]

    - type: surface
      physics: surface_force_and_moment
      output_file_name: topwall.dat
      frequency: 100
      parameters: [0,0]
      target_name: [topwall]

    output:
      output_data_base_name: results/channelFlow.e
      output_frequency: 100
      output_node_set: no
      output_variables:
       - velocity
       - pressure
       - pressure_force
       - tau_wall

    restart:
      restart_data_base_name: restart/channelFlow.rst
      output_frequency: 5000

Time_Integrators:
  - StandardTimeIntegrator:
      name: ti_1
      start_time: 0
      time_step: 0.5
      termination_time: 4635
      time_stepping_type: adaptive
      time_step_count: 0
      second_order_accuracy: yes

      realms:
        - realm_1
