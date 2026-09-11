from drone import Drone


class Zone:
    """
    Represents a zone in the drone simulation graph.

    A zone has a position, a type, a visual color, and a maximum drone
    capacity. It also tracks the drones currently occupying the zone and
    drones that are temporarily entering through a restricted connection.

    Attributes:
        name (str): The unique name of the zone.
        x (int): The horizontal coordinate of the zone.
        y (int): The vertical coordinate of the zone.
        zone (str): The type of zone, such as "normal", "priority", or
            "restricted".
        color (str): The color used to display the zone.
        max_drone (int): The maximum number of drones that can occupy
            the zone.
        current_occupancy (list[Drone]): The drones currently occupying
            the zone.
        weight (float): The calculated distance or cost from the zone to
            the destination hub. Defaults to infinity.
        in_link (list[Drone]): The drones currently entering the zone through
            a restricted connection.
    """
    def __init__(self, name: str, coordinate_x: int, coordinate_y: int,
                 zone: str = "normal", color: str = "blue", max_drone: int = 1,
                 current_occupancy: list[Drone] = []) -> None:
        """
        Initialize a zone.

        Args:
            name (str): The unique name of the zone.
            coordinate_x (int): The horizontal coordinate of the zone.
            coordinate_y (int): The vertical coordinate of the zone.
            zone (str, optional): The type of zone. Defaults to "normal".
            color (str, optional): The display color of the zone.
                Defaults to "blue".
            max_drone (int, optional): The maximum number of drones that
                can occupy the zone. Defaults to 1.
            current_occupancy (list[Drone], optional): The drones initially
                occupying the zone. Defaults to an empty list.
        """
        self.name: str = name
        self.x: int = coordinate_x
        self.y: int = coordinate_y
        self.zone: str = zone
        self.color: str = color
        self.max_drone: int = max_drone
        self.current_occupancy: list[Drone] = current_occupancy
        self.weight = float('inf')
        self.in_link: list[Drone] = []

    def capacity_checking(self) -> bool:
        """
        Check whether the zone can accept another drone.

        Returns:
            bool: True if the current occupancy is below the maximum
                capacity, otherwise False.
        """
        return len(self.current_occupancy) < self.max_drone

    def restricted_link_checking(self) -> bool:
        """
        Check whether a drone can enter through a restricted link.

        Returns:
            bool: True if the number of drones currently entering through
                the restricted link is below the zone's maximum capacity,
                otherwise False.
        """
        return len(self.in_link) < self.max_drone
