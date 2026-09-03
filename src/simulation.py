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
            hub_min = sorted(neighbours, key=lambda n: (n.weight, n.zone != "priority"))[0]
            if hub_min.zone == "restricted":
                connection = self.graph.retrieve_connection_by_zones([current_hub, hub_min])
                connection.drone.append(self.drone)
            hub_min.current_occupancy.append(self.drone)
            current_hub.current_occupancy.remove(self.drone)
            if connection.drone != []:
                print(f"D{self.drone.id}-{connection.zones[0].name}-{connection.zones[1].name}")
                connection.drone.remove(self.drone)
            print(f"D{self.drone.id}-{hub_min.name}")
            self.drone.current_zone = hub_min.name
