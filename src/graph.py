from .zone import Zone
from .connection import Connection
from collections import Counter


class Graph:
    """
    Represents a graph composed of zones and connections.

    The graph manages a collection of zones and the connections between them.
    It also keeps track of the number of start and end hubs to ensure that
    the graph contains exactly one of each.
    """
    def __init__(self, zones: list[Zone],
                 connections: list[Connection]) -> None:
        """
        Initializes a graph with a collection of zones and connections.

        Args:
            zones (list[Zone]): The zones that make up the graph.
            connections (list[Connection]): The connections between the zones.
        """
        self.zones: list[Zone] = zones
        self.connections: list[Connection] = connections
        self.count_end: int = 0
        self.count_start: int = 0
        self.start_hub: str = ""
        self.end_hub: str = ""

    def retrieve_zone_by_name(self, zone_name: str) -> Zone | None:
        """
        Retrieves a zone based on its name.

        Searches through the collection of zones and returns the zone
        whose name matches the given name. Returns None if no matching
        zone is found.

        Args:
            zone_name (str): The name of the zone to retrieve.

        Returns:
            Zone | None: The matching zone, or None if no zone is found.
        """
        for zone in self.zones:
            if zone.name == zone_name:
                return zone
        return None

    def retrieve_zone_by_position(self, x: int, y: int) -> Zone | None:
        """
        Retrieves a zone based on its position.

        Searches through the collection of zones and returns the zone
        whose coordinates match the given x and y values. Returns None
        if no zone is found at the specified position.

        Args:
            x (int): The x-coordinate of the zone.
            y (int): The y-coordinate of the zone.

        Returns:
            Zone | None: The zone found at the specified position,
            or None if no matching zone exists.
        """
        for element in self.zones:
            if element.x == x and element.y == y:
                return element
        return None

    def add_zone(self, zone: Zone) -> None:
        """
        Adds a zone to the collection.

        Checks whether a zone with the same name already exists before adding
        the new zone. Raises a ValueError if a duplicate zone is detected.

        Args:
            zone (Zone): The zone to add.

        Raises:
            ValueError: If a zone with the same name already exists.
        """
        if self.retrieve_zone_by_name(zone.name):
            raise ValueError(f"[ERROR]: zone '{zone.name}' is duplicate.")
        if self.retrieve_zone_by_position(zone.x, zone.y):
            raise ValueError(f"[ERROR]: coordinates of '{zone.name}' already exist.")
        self.zones.append(zone)

    def retrieve_connection_by_zones(self, zones: list[Zone]) -> Connection | None:
        """
        Retrieves a connection between the specified zones.

        Searches through the collection of connections and returns the connection
        whose zones match the given zones, regardless of their order. Returns None
        if no matching connection is found.

        Args:
            zones (list[Zone]): The zones associated with the connection.

        Returns:
            Connection | None: The matching connection, or None if no connection
            exists between the specified zones.
        """
        for element in self.connections:
            if Counter(element.zones) == Counter(zones):
                return element
        return None

    def add_connection(self, connection: Connection) -> None:
        """
        Adds a connection to the collection.

        Checks whether a connection between the same zones already exists
        before adding the new connection. Raises a ValueError if a duplicate
        connection is detected.

        Args:
            connection (Connection): The connection to add.

        Raises:
            ValueError: If a connection between the specified zones already exists.
        """
        if self.retrieve_connection_by_zones(connection.zones):
            raise ValueError(f"[ERROR]: connection between "
                             f"'{connection.zones[0].name}' and '{connection.zones[1].name}' "
                             f"already exists.")
        self.connections.append(connection)

    def validate_end_start_hub(self) -> None:
        """
        Validates the start and end hubs of the network.

        Ensures that exactly one start hub and exactly one end hub are defined.
        Raises a ValueError if either hub is duplicated or missing.

        Raises:
            ValueError: If there are multiple start or end hubs, or if either
            the start hub or end hub is missing.
        """
        if self.count_start > 1:
            raise ValueError("[ERROR]: start_hub duplicate")
        if self.count_end > 1:
            raise ValueError("[ERROR]: end_hub duplicate")
        if self.count_start == 0:
            raise ValueError("[ERROR]: missing start_hub")
        if self.count_end == 0:
            raise ValueError("[ERROR]: missing end_hub")

    def retrieve_neighbour(self, zone: Zone) -> list[Zone]:
        """
        summary
        """
        neighbours: list[Zone] = []
        for connex in self.connections:
            for hub in connex.zones:
                if hub.name == zone.name:
                    neighbours = list(set(neighbours + connex.zones))
        return neighbours

    def put_zone_weight(self, zone: Zone) -> None:
        """
        summary
        """
        neighbours = self.retrieve_neighbour(zone)
        for hub in neighbours:
            weight = 1
            if hub.zone == "restricted":
                weight = 2
            if hub.zone == "blocked":
                continue
            if hub.weight > zone.weight + weight:
                hub.weight = zone.weight + weight
                self.put_zone_weight(hub)
