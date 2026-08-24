
class Zone:
    """
    _summary_
    """
    def __init__(self, name: str, coordinate_x: int, coordinate_y: int,
                 zone: str, color: str, max_drone: str, current_occupancy: list) -> None:
        """_summary_

        Args:
            name (str): _description_
            coordinate_x (int): _description_
            coordinate_y (int): _description_
            zone (str): _description_
            color (str): _description_
            max_drone (str): _description_
        """
        self.name: str = name
        self.x: int = coordinate_x
        self.y: int = coordinate_y
        self.zone: str = zone
        self.color: str = color
        self.max_drone: str = max_drone
        self.current_occupancy: list = current_occupancy

    def capacity_checking(self) -> None:
        """
        _summary_
        """
        pass

    def entering_zone(self) -> None:
        """
        _summary_
        """
        pass

    def leaving_zone(self) -> None:
        """
        _summary_
        """
        pass
