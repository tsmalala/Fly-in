import sys
import pygame as py
from graph import Graph
from parser import Parser
from simulation import Simulation
from visualisation import Visualisation


def main() -> None:
    """
    Initialize and run the Fly-in drone simulation.

    The function validates the command-line arguments, parses the input file
    to construct the simulation graph, calculates the zone weights from the
    destination hub, and initializes the drone simulation.

    It then initializes Pygame, creates the visualization window, starts the
    graphical simulation, and properly shuts down Pygame when the visualization
    is closed.

    Raises:
        ValueError: If the program is not provided with exactly one
            command-line argument.
    """
    graph = Graph([], [], 0)
    if len(sys.argv) != 2:
        raise ValueError("[ERROR]: arguments error!")
    Parser.parse_file(sys.argv[1], graph)
    for element in graph.zones:
        if element.name == graph.end_hub:
            element.weight = 0
    end_hub = graph.retrieve_zone_by_name(graph.end_hub)
    if end_hub is None:
        return
    graph.put_zone_weight(end_hub)
    start_hub = graph.retrieve_zone_by_name(graph.start_hub)
    if start_hub:
        if start_hub.weight == float('inf'):
            raise ValueError("[ERROR]: No path between start and end")
    simulation = Simulation(graph)

    py.init()

    WINDOW_WIDTH = 1800
    WINDOW_HEIGHT = 900

    window = py.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    py.display.set_caption("Fly-in")

    visualize = Visualisation(simulation, window, WINDOW_WIDTH, WINDOW_HEIGHT)
    visualize.visualizer()

    py.quit()


if __name__ == "__main__":
    try:
        main()
    except ValueError as e:
        print(e)
