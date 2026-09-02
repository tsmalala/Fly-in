from .zone import Zone
from .connection import Connection
from .graph import Graph
import re


class Parser:
    """
    Parse a configuration file and build the corresponding graph.

    The parser supports configuration entries for the number of drones,
    hubs, start and end hubs, and connections between hubs.
    """
    @staticmethod
    def parse_file(filename: str, graph: Graph) -> None:
        """
        Parse a configuration file and update the graph.

        The file is read line by line. Empty lines and comments starting
        with ``#`` are ignored. Each valid configuration line is parsed
        and applied to the provided graph.

        Args:
            filename: Path to the configuration file to parse.
            graph: Graph instance to update with the parsed configuration.

        Raises:
            ValueError: If a configuration line contains invalid syntax
                or invalid data.
            OSError: If the file cannot be opened or read.
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
        Parse a configuration line and update the graph accordingly.

        The line must follow the format ``<type>:<data>``.
        Supported line types are ``nb_drones``, ``hub``, ``start_hub``,
        ``end_hub`` and ``connection``.

        Args:
            line: Configuration line to parse.
            graph: Graph instance to update with the parsed data.

        Raises:
            ValueError: If the line has an invalid syntax, contains an
            unknown type, or contains invalid data.
        """
        try:
            _type, data = line.split(":")
        except ValueError as e:
            raise ValueError(f"[ERROR]: {e}")

        if _type == "nb_drones":
            Parser._parse_nb_drones(data)
            return

        if _type in ["hub", "start_hub", "end_hub"]:
            Parser._parse_hub_syntax(data, _type, graph)
            return

        if _type == "connection":
            connection = Parser.parse_connection(data, graph)
            graph.add_connection(connection)
            return

        raise ValueError(f"[ERROR]: unknown line type '{_type}'!")

    @staticmethod
    def _parse_nb_drones(data: str) -> None:
        """
        Validate the number of drones specified in the configuration.

        The provided value must be a strictly positive integer.

        Args:
            data: String representation of the number of drones.

        Raises:
            ValueError: If ``data`` is not an integer or if the value
                is not strictly positive.
        """

        try:
            nb = int(data)
        except ValueError:
            raise ValueError("[ERROR]'nb_drones' must be an integer!")
        if nb <= 0:
            raise ValueError("[ERROR]: nb_drones must be strictly positive.")

    @staticmethod
    def _parse_hub_syntax(data: str, hub_type: str, graph: Graph) -> None:
        """
        Parse a hub configuration and add the hub to the graph.

        The hub type is used to update the corresponding start or end hub
        counter before the hub is parsed and added to the graph.

        Args:
            data: Hub configuration data containing its name,
                coordinates and optional metadata.
            type: Type of hub being parsed. Expected values are
                ``hub``, ``start_hub`` or ``end_hub``.
            graph: Graph instance to which the parsed hub is added.

        Raises:
            ValueError: If the hub configuration contains invalid syntax
                or invalid data.
        """
        if hub_type == "start_hub":
            graph.count_start += 1
            hub = Parser.parse_hub(data, graph, hub_type)
        elif hub_type == "end_hub":
            hub = Parser.parse_hub(data, graph, hub_type)
            graph.count_end += 1
        else:
            hub = Parser.parse_hub(data, graph)
        graph.add_zone(hub)

    @staticmethod
    def parse_hub(data: str, graph: Graph, special_hub: str = "") -> Zone:
        """
        Parse a hub configuration and create a Zone instance.

        The expected format contains a hub name followed by its X and Y
        coordinates. Optional metadata can be provided between square
        brackets, including ``zone``, ``color`` and ``max_drones``.

        Example:
            ``hub1 10 20 [zone=priority color=red max_drones=5]``

        Args:
            data: String containing the hub name, coordinates and
                optional metadata.

        Returns:
            A Zone instance initialized with the parsed configuration.

        Raises:
            ValueError: If the hub name contains ``-``, if the coordinates
                are not integers, or if the metadata contains invalid
                values or an unsupported zone type.
            IndexError: If the hub configuration does not contain enough
                elements for a name and two coordinates.
        """
        match = re.search(r"\[([^\]]+)\]", data)
        clean_data = re.sub(r"\[([^\]]+)\]", "", data)
        data_splited: list[str] = clean_data.split()
        name = data_splited[0]
        if special_hub:
            if special_hub == "start_hub":
                graph.start_hub = name
            elif special_hub == "end_hub":
                graph.end_hub = name
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
        Parse a connection configuration and create a Connection instance.

        A connection consists of two or more existing hubs separated by
        ``-``. An optional ``max_link_capacity`` metadata value can be
        specified between square brackets.

        Example:
            ``hub1-hub2 [max_link_capacity=10]``

        Args:
            data: String containing the hub names and optional connection
                metadata.
            graph: Graph instance used to retrieve the hubs referenced
                by the connection.

        Returns:
            A Connection instance containing the parsed hubs and its
            maximum link capacity.

        Raises:
            ValueError: If a referenced hub does not exist or if
                ``max_link_capacity`` is not a valid integer.
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
