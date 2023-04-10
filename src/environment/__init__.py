"""
This module defines the various custom gym/gymnasium environments.
Each environment defines BugPlus:
    - observation_space: The observation space of the environment.
    - action_space: The action space of the environment.
    - reset: Resets the environment to its original state and loads a new configuration.
    - step: Executes one step in the environment.
    - check_bug_validity: Checks if the structure built by the agent is valid and defines rewards if not.
    - set_input_output_state: Sets the input and output state of the environment.
    - set_matrix_state: Sets the matrix state of the environment.
"""