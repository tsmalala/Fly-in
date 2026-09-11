from zone import Zone
from drone import Drone


class Connection:
    """
    Represents a connection between multiple zones.

    A connection defines the zones that are linked together and the maximum
    capacity of the link. It can also keep track of drones associated with
    the connection.

    Attributes:
        zones (list[Zone]): The zones connected by this connection.
        max_link_capacity (int): The maximum number of drones or links that
            can be supported by the connection.
        drone (list): The drones currently associated with the connection.
    """
    def __init__(self, zones: list[Zone], max_link_capacity: int = 1) -> None:
        """
        Initialize a Connection.

        Args:
            zones (list[Zone]): The zones to be connected.
            max_link_capacity (int, optional): Maximum capacity of the
                connection. Defaults to 1.
        """
        self.zones: list[Zone] = zones
        self.max_link_capacity: int = max_link_capacity
        self.drone: list[Drone] = []
