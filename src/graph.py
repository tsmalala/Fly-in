from .zone import Zone
from .connection import Connection


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

    def adjacency_lists(self) -> None:
        """
        _summary_
        """
        pass

    def add_zone(self, zone: Zone) -> None:
        """
        _summary_
        """
        self.zones.append(zone)

    def add_connection(self, connection: Connection) -> None:
        """
        _summary_
        """
        self.connections.append(connection)

    def retrieve_zone_by_name(self, zone_name: str) -> Zone | None:
        """
        Retrieve a zone by its name.
        """
        for zone in self.zones:
            if zone.name == zone_name:
                return zone
        return None

    def retrieve_neighbours(self) -> None:
        """
        _summary_
        """
        pass

    def check_duplication(self) -> None:
        pass

    def validate_end_start_hub(self) -> None:
        if self.count_start > 1:
            raise ValueError("[ERROR]: start_hub duplicate")
        if self.count_end > 1:
            raise ValueError("[ERROR]: end_hub duplicate")
