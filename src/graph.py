from src.zone import Zone
from src.connection import Connection


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

    def adjacency_lists(self) -> None:
        """
        _summary_
        """
        pass

    def add_zone(self) -> None:
        """
        _summary_
        """
        pass

    def add_connection(self) -> None:
        """
        _summary_
        """
        pass

    def retrieve_zone(self) -> None:
        """
        _summary_
        """
        pass

    def retrieve_neighbours(self) -> None:
        """
        _summary_
        """
        pass
