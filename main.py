from src.parser import Parser
from src.graph import Graph


def main() -> None:
    graph = Graph([], [], 0)
    Parser.parse_file("config.txt", graph)
    for element in graph.zones:
        if element.name == graph.end_hub:
            element.weight = 0
    graph.put_zone_weight(graph.retrieve_zone_by_name(graph.end_hub))
    for e in graph.zones:
        print(f"Name: {e.name}, weight: {e.weight}")
    print(graph.nb_drone)


if __name__ == "__main__":
    try:
        main()
    except ValueError as e:
        print(e)
        