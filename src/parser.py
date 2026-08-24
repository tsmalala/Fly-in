from .zone import Zone
from .connection import Connection


class Parser:
    def parse(self, line: str) -> None:
        hub_parsed: list[Zone] = []
        connection_parsed: list[Connection] = []

        clean_line = line.strip()

        if not clean_line or clean_line.startswith('#'):
            pass
        
        if line.startswith("nb_drones"):
            try:
                key, value = line.split(":")
                nb_drone = int(value)
            except ValueError:
                raise ValueError(f"Nombre de drones invalide : {line}")

        if line.startswith("start_hub"):
            start_value: list = line.split()
            
        if line.startswith("end_hub"):
            end_value: list = line.split()
            
        if line.startswith("hubs"):
            pass

        if line.startswith("connection"):
            pass
