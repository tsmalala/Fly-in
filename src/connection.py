from .drone import Drone
from .zone import Zone


class Connection:
    """
    _summary_
    """
    def __init__(self, zones: list[Zone], max_link_capacity: int = 1) -> None:
        """_summary_
        Args:
            zones (str): _description_
            link (str): _description_
        """
        self.zones: list[Zone] = zones
        self.max_link_capacity: int = max_link_capacity
        self.drone: list = []

    def drones_tracker(self) -> None:
        """
        _summary_
        """
        pass

    def capacity_trackers(self) -> None:
        """
        _summary_
        """
        pass

    def connection_traversal(self) -> None:
        """
        _summary_
        """
        pass
