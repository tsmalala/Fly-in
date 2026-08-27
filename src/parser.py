from .zone import Zone
from .connection import Connection
from .graph import Graph
import re


class Parser:
    """
    _summary_
    """
    @staticmethod
    def parse_file(filename: str, graph: Graph) -> None:
        """
        _summary_
        """
        with open(filename, "r") as file:
            for line in file:
                line = line.strip()
                line = re.sub(r"#.*", "", line)
                if not line:
                    continue
                Parser.parse_line(line, graph)
        graph.validate_end_start_hub()

    @staticmethod
    def parse_line(line: str, graph: Graph) -> None:
        """
        _summary_
        """
        _type, data = line.split(":")
        if _type == "nb_drones":
            try:
                nb = int(data)
            except ValueError:
                raise ValueError("[ERROR]'nb_drones' must be an integer!")
            if nb <= 0:
                raise ValueError("[ERROR]: nb_drones must be strictly positive.")
        if "hub" in _type:
            if "start" in _type:
                graph.count_start += 1
            if "end" in _type:
                graph.count_end += 1
            hub = Parser.parse_hub(data)
            graph.add_zone(hub)
        if "connection" in _type:
            connection = Parser.parse_connection(data, graph)
            graph.add_connection(connection)

    @staticmethod
    def parse_hub(data: str) -> Zone:
        """
        _summary_
        """
        match = re.search(r"\[([^\]]+)\]", data)
        clean_data = re.sub(r"\[([^\]]+)\]", "", data)
        data_splited: list[str] = clean_data.split()
        name = data_splited[0]
        if "-" in name:
            raise ValueError("[ERROR]: name can't contain '-'.")
        try:
            x = int(data_splited[1])
        except ValueError:
            raise ValueError("[ERROR] Coordinate x must be an integer!")
        try:
            y = int(data_splited[2])
        except ValueError:
            raise ValueError("[ERROR] Coordinate y must be an integer!")
        zone = ""
        color = ""
        max_drones = 0
        if match:
            metadata = match.group(1)
            list_medata = metadata.split()
            for e in list_medata:
                if "zone" in e:
                    zone = e.split("=")[1]
                    if zone not in ["restricted", "normal", "priority",
                                    "blocked"]:
                        raise ValueError("[ERROR]: zone type not valid")
                elif "color" in e:
                    color = e.split("=")[1]
                elif "max_drones" in e:
                    try:
                        max_drones = int(e.split("=")[1])
                    except ValueError:
                        raise ValueError("[ERROR] max_drones must be an "
                                         "integer!")
                    else:
                        if max_drones <= 0:
                            raise ValueError("[ERROR]: max_drones must be positive")
                else:
                    raise ValueError("[ERROR] invalid metadata")
        return Zone(name, x, y, zone, color, max_drones)

    @staticmethod
    def parse_connection(data: str, graph: Graph) -> Connection:
        """
        _summary_
        """
        clean_data = re.sub(r"\[([^\]]+)\]", "", data)
        hubs = clean_data.split("-")
        zones_list: list[Zone] = []
        for hub in hubs:
            hub = hub.strip()
            name = graph.retrieve_zone_by_name(hub)
            if name is not None:
                zones_list.append(name)
            else:
                raise ValueError(f"[ERROR]: {hub} doesn't exit")
        
        match = re.search(r"\[([^\]]+)\]", data)
        max_link_capacity = 1
        if match:
            metadata = match.group(1)
            if "max_link_capacity" in metadata:
                try:
                    max_link_capacity = int(metadata.split("=")[1])
                except ValueError:
                    raise ValueError("[ERROR] max_link_capacity must be an "
                                     "integer!")
        return Connection(zones_list, max_link_capacity)
