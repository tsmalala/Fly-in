
class Drone:
    """
    Represents a drone operating between different zones.

    A drone has a unique identifier, a current zone, and an optional
    destination hub that it is scheduled to travel to.

    Attributes:
        id (int): The unique identifier of the drone.
        current_zone (str): The zone where the drone is currently located.
        next_hub (Zone | None): The next hub or zone the drone is scheduled
            to travel to. Defaults to None.
    """
    def __init__(self, id: int, current_zone: str) -> None:
        """
        Initialize a Drone.

        Args:
            id (int): The unique identifier assigned to the drone.
            current_zone (str): The zone where the drone is initially located.
        """
        from zone import Zone
        self.id: int = id
        self.current_zone: str = current_zone
        self.next_hub: Zone | None = None
