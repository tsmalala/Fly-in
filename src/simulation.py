from .graph import Graph
from .drone import Drone

class Simulation:
    """
    """
    def __init__(self, graph: Graph) -> None:
        """
        """
        self.graph: Graph = graph
        all_drone: list[Drone] = []
        for i in range(0, graph.nb_drone):
            drone = Drone(i + 1, graph.start_hub)
            all_drone.append(drone)
        zone = graph.retrieve_zone_by_name(graph.start_hub)
        for drone in all_drone:
            self.drone = drone
            zone.current_occupancy.append(drone)
            drone.current_zone = zone.name
        self.all_drone = all_drone

    def simulate(self) -> None:
        """
        """
        end_zone = self.graph.retrieve_zone_by_name(self.graph.end_hub)
        while len(end_zone.current_occupancy) < self.graph.nb_drone:
            move: list[str] = []
            for drone in self.all_drone:
                current_zone = self.graph.retrieve_zone_by_name(drone.current_zone)
                neighbours = self.graph.retrieve_neighbour(current_zone)
                next_hub = sorted(neighbours, key=lambda n: (n.weight, n.zone != "priority"))[0]
                # current_connection = self.graph.retrieve_connection_by_zones([next_hub, current_zone])
                if (next_hub.current_occupancy == []) or next_hub.name == self.graph.end_hub:
                    next_hub.current_occupancy.append(drone)
                    drone.current_zone = next_hub.name
                    current_zone.current_occupancy.remove(drone)
                    move.append(f"D{drone.id}-{drone.current_zone}")
            print(" ".join(move))
