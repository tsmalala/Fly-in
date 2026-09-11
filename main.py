import sys
from parser import Parser
from graph import Graph
from simulation import Simulation


def main() -> None:
    """
    Run the drone simulation from the command-line input file.

    The function validates the command-line arguments, parses the input file
    to build the simulation graph, initializes the destination hub's weight,
    and starts the drone simulation.

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
    simulation.simulate()


if __name__ == "__main__":
    try:
        main()
    except ValueError as e:
        print(e)
