from .graph import Graph
from .drone import Drone

class Simulation:
    """
    """
    def __init__(self, graph: Graph) -> None:
        """
        """
        self.graph: Graph = graph
        drone = Drone(1, graph.start_hub)
        self.drone = drone
        zone = graph.retrieve_zone_by_name(graph.start_hub)
        zone.current_occupancy.append(drone)

    def simulate(self) -> None:
        """
        """
        while self.drone.current_zone != self.graph.end_hub:
            current_hub = self.graph.retrieve_zone_by_name(self.drone.current_zone)
            neighbours = self.graph.retrieve_neighbour(current_hub)
            min = float('inf')
            for hub in neighbours:
                if hub.weight < min:
                    min = hub.weight
                    hub_min = hub
            hub_min.current_occupancy.append(self.drone)
            current_hub.current_occupancy.remove(self.drone)
            print(f"D{self.drone.id}-{hub_min.name}")
            self.drone.current_zone = hub_min.name
