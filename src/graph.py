from .zone import Zone
from .connection import Connection
from collections import Counter


class Graph:
    """
    _summary_
    """
    def __init__(self, zones: list[Zone],
                 connections: list[Connection]) -> None:
        """_summary_

        Args:
            zones (list[Zone]): _description_
            connections (list[Connection]): _description_
        """
        self.zones: list[Zone] = zones
        self.connections: list[Connection] = connections
        self.count_end: int = 0
        self.count_start: int = 0

    def retrieve_zone_by_name(self, zone_name: str) -> Zone | None:
        """
        Retrieve a zone by its name.
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
        """
        if self.retrieve_zone_by_name(zone.name):
            raise ValueError(f"[ERROR]: zone '{zone.name}' is dublicate.")
        if self.retrieve_zone_by_position(zone.x, zone.y):
            raise ValueError(f"[ERROR]: coordinates of '{zone.name}' already exist.")
        self.zones.append(zone)

    def retrieve_connection_by_zones(self, zones: list[Zone]) -> Connection | None:
        """
        Retrieves a connection between the specified zones.

        Searches through the collection of connections and returns the connection
        whose zones match the given zones, regardless of their order. Returns None
        if no matching connection is found.
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
            raise ValueError(f"[ERROR]: {connection.zones[0].name}-{connection.zones[1].name} connection is duplicate.")
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
