from src.parser import Parser
from src.graph import Graph
from src.simulation import Simulation

def main() -> None:
    graph = Graph([], [], 0)
    Parser.parse_file("config.txt", graph)
    for element in graph.zones:
        if element.name == graph.end_hub:
            element.weight = 0
    graph.put_zone_weight(graph.retrieve_zone_by_name(graph.end_hub))
    simulation = Simulation(graph)

    simulation.simulate()


if __name__ == "__main__":
    try:
        main()
    except ValueError as e:
        print(e)
        