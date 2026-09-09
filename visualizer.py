import sys
import pygame as py
from src.parser import Parser
from src.graph import Graph
from src.simulation import Simulation
from src.visualisation import Visualisation


def main() -> None:
    graph = Graph([], [], 0)
    if len(sys.argv) != 2:
        raise ValueError("[ERROR]: arguments error!")
    Parser.parse_file(sys.argv[1], graph)
    for element in graph.zones:
        if element.name == graph.end_hub:
            element.weight = 0
    graph.put_zone_weight(graph.retrieve_zone_by_name(graph.end_hub))
    simulation = Simulation(graph)

    py.init()

    WINDOW_WIDTH = 1600
    WINDOW_HEIGHT = 800

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
