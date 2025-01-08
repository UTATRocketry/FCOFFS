# Solver Output Handling
An output handler class which handles all forms of output for the software is attached to the solver class when initialized. The output from the solvers can be customized through the output handler, and this file will outline the capabilities and customizations available for solution output. 

## Output Handler Capabilities
The main features of the output handler are:
 + Steady State Solver
   - Present the final converged solution in the terminal
   - Present system state/guess at each convergence step along with the steps root mean squared residual in the terminal
   - Create log files of the system's state at each convergence step. Three separate logs are created: one focused on interfaces, one on components, and one that contains everything. The logs are saved as .log files and are in comma-separated format. 
   - Provide the most recent state and convergence output when the solver breaks during convergence and error information to the terminal.
   - Show the system tree in the terminal
 + Transient State Solver
   - Present the converged state of the system at the last time step to the terminal
   - Present each converged state of the system at each time step to the terminal along with the root mean square of the residual
   - Allows users to add specific probes to be monitored and stored throughout all time steps. Can probe an object/variable inside any component or interface.
   - Present a table of all probes and their values over time to the terminal.
   - Create log files of the system's state at each convergence step over all time steps. Three separate logs are created: one focused on interfaces, one on components, and one that contains everything. The logs are saved as .log files and are in comma-separated format. If any probes exist, a log file is also created of them throughout time.
   - Provide error information if the solver breaks such as the last state/guess of the system and the error which caused the execution break
   - Plot probe constituents over time after the solver has finished running using matplotlib
   - Show the system tree in the terminal

## Ouput Handler Customization
When it comes to cstomizing /configuring the output handler you must do it through the solver object. TO access any output commands you must use solverobject.ouput

A very important key command to know is showing the current output handler configurations. 
