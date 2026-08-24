
class Drone:
    """
    _summary_
    """
    def __init__(self, id: int, current_zone: str, current_path: str,
                 path_position: str, status: str) -> None:
        """_summary_

        Args:
            id (int): _description_
            current_zone (str): _description_
            current_path (str): _description_
            path_position (str): _description_
            status (str): _description_
        """
        self.id: int = id
        self.current_zone: str = current_zone
        self.current_path: str = current_path
        self.path_position: str = path_position
        self.status: str = status

    def define_status(self) -> None:
        """
        _summary_
        """
        pass
