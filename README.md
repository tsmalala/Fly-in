*This project has been created as part of the 42 curriculum by tsmalala.*

# Fly-in

## Description

This project is a drone-routing simulation built around a graph of hubs and connections.

The goal is to parse a custom configuration file, construct the corresponding graph, simulate the movement of multiple drones from a start hub to an end hub, and provide a real-time graphical representation of the simulation.

The project combines several concepts:

- **Hubs (`Zone`)** represent locations in the graph. Each hub has a name, coordinates, a zone type, a display color, and a maximum number of drones it can hold.
- **Connections (`Connection`)** represent links between hubs and may define a maximum link capacity.
- **The graph (`Graph`)** stores hubs and connections and provides validation and lookup operations.
- **Drones (`Drone`)** represent the moving agents in the simulation.
- **The simulation (`Simulation`)** is responsible for advancing drones through the graph.
- **The parser (`Parser`)** validates the configuration file and converts it into graph objects.
- **The visualizer (`Visualisation`)** uses Pygame to display hubs, connections, and drones while the simulation is running.

The application therefore combines file parsing, graph modelling, routing, capacity constraints, simulation logic, and an interactive graphical interface.

## Features

- Custom configuration-file parser.
- Support for comments and empty lines.
- Validation of the number of drones.
- Start and end hub management.
- Hub coordinates and visual metadata.
- Four zone types:
  - `normal`
  - `priority`
  - `restricted`
  - `blocked`
- Maximum drone capacity per hub.
- Maximum capacity per connection.
- Graph-based drone simulation.
- Real-time Pygame visualization.
- Horizontal and vertical scrolling.
- Large virtual world for displaying maps with distant coordinates.
- Visual separation of drones occupying the same hub.
- Automatic simulation advancement once per second.
- Terminal output showing drone movements.
- Display of the total number of turns when the visualization is closed.

## Instructions

Intsall depedancies:

    make install

Activate the virtual environnement:

    source .venv/bin/activate

Run the program main:

    make run

## Resources

### Documentation and References

The following resources were used to understand the technologies and concepts involved in the project:

- **Python Documentation**  
  https://docs.python.org/3/  
  Used as a reference for Python syntax, file handling, exceptions, data structures, and standard library features.

- **Python `re` Module Documentation**  
  https://docs.python.org/3/library/re.html  
  Used to understand regular expressions for parsing configuration files and extracting metadata from hubs and connections.

- **Pygame Documentation**  
  https://www.pygame.org/docs/  
  Used as the main reference for the graphical interface, surfaces, images, events, rendering, and window management.

- **Pygame Drawing Documentation**  
  https://www.pygame.org/docs/ref/draw.html  
  Used for drawing connections between hubs and other graphical elements.

- **Pygame Event Documentation**  
  https://www.pygame.org/docs/ref/event.html  
  Used to handle user interactions such as closing the window, mouse clicks, and scrolling.

- **Pygame Surface Documentation**  
  https://www.pygame.org/docs/ref/surface.html  
  Used for manipulating and displaying graphical assets.


### AI Usage

AI was used as documentation assistant during the project.

The following tasks were supported by AI:

- **Pygame documentation:** AI helped explain the purpose of the Pygame rendering, event handling, image manipulation, scrolling system, and coordinate transformations implemented in `visualisation.py`.

AI was used as a support tool for understanding, reviewing, explaining, and documenting the project.

## Algorithm Choices and Implementation Strategy

The project models the drone transportation problem as a graph.

Each hub is represented by a `Zone` object and each connection between hubs is represented by a `Connection` object. Drones move through this graph from a start hub to an end hub while respecting the constraints defined by the configuration.


###  Algorithm Choices and Implementation

The project models the drone transportation system as a graph. Hubs are represented as vertices (`Zone`) and connections as edges (`Connection`). The `Graph` class stores these elements and provides the operations required by the simulation.

The implementation is divided into several independent stages. First, the `Parser` reads the configuration file line by line, removes comments and empty lines, validates the input, and creates the corresponding graph objects. Regular expressions are used to extract optional metadata such as zone type, color, and capacity. Invalid data is rejected immediately to prevent inconsistent states from reaching the simulation.

Once the graph has been constructed and validated, the `Simulation` class manages drone movements. At each simulation turn, the available connection capacities are provided to the simulation. The movement algorithm determines which drones can move while respecting the graph constraints, including hub occupancy and connection capacities. The simulation is executed turn by turn until all drones reach the destination hub.

The graphical layer is deliberately separated from the simulation logic. The `Visualisation` class is responsible only for displaying the current state and handling user interaction. Hubs are positioned using their graph coordinates, connections are drawn as lines between hubs, and drones are displayed at their current locations. When several drones occupy the same hub, their positions are offset to prevent them from overlapping completely.

The visualization also implements horizontal and vertical scrolling over a large virtual world. Graph coordinates are converted into screen coordinates using the hub tile size and the current scroll offsets. The background is tiled to provide a continuous visual environment while navigating the map.

The simulation advances approximately once per second, allowing the user to observe each turn and follow the movement of the drones. The movements are printed in the terminal while the Pygame interface provides a real-time visual representation.

The overall strategy is therefore based on three main principles: representing the network as a graph, separating simulation logic from presentation logic, and processing drone movements incrementally while respecting capacity constraints. This modular approach makes the project easier to understand, maintain, test, and extend.


### Visual Representation and User Experience

The project includes a Pygame-based graphical interface designed to make the drone simulation easier to understand.

Instead of displaying only textual movements, the user can observe the graph and the drones moving through it in real time.

The main advantage is that drones remain individually visible even when several of them occupy the same hub.

#### User Experience Benefits

The visualization improves the user experience by:

1. Making the graph topology immediately visible.
2. Making the start and end hubs easier to identify through colors.
3. Showing the current position of every drone.
4. Preventing overlapping drones from becoming impossible to distinguish.
5. Providing a visual representation of connections.
6. Allowing the user to explore large maps using scrolling.
7. Animating the simulation step by step.
8. Combining graphical information with terminal output containing the exact movements.

### Example Input

The following configuration demonstrates the main features of the program:

    ```
    # Number of drones
    nb_drones:3

    # Start hub
    start_hub:A 0 0 [zone=priority color=green max_drones=3]

    # Intermediate hubs
    hub:B 2 0 [zone=normal color=blue max_drones=2]
    hub:C 2 2 [zone=normal color=blue max_drones=2]

    # End hub
    end_hub:D 4 2 [zone=normal color=red max_drones=3]

    # Connections
    connection:A-B [max_link_capacity=2]
    connection:B-C [max_link_capacity=2]
    connection:C-D [max_link_capacity=2]

### Expected Output

The program prints the movements performed during each simulation turn.

    ```
    D1-B D2-B
    D1-C D2-C D3-B
    D1-D D2-D D3-C

    Total turns: 4


### Requirements

The project requires:

- Python 3
- Pygame

