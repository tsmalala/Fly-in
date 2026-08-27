from src.parser import Parser
from src.graph import Graph


def main() -> None:
    graph = Graph([], [])
    Parser.parse_file("config.txt", graph)
    print(graph.zones)
    print(graph.connections)


if __name__ == "__main__":
    try:
        main()
    except ValueError as e:
        print(e)
        