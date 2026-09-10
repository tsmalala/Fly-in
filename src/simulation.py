from .graph import Graph
from .drone import Drone
from .connection import Connection


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
        nb_turn = 0
        end_zone = self.graph.retrieve_zone_by_name(self.graph.end_hub)

        while len(end_zone.current_occupancy) < self.graph.nb_drone:
            move: list[str] = []
            link_capacity = {connection: connection.max_link_capacity
                             for connection in self.graph.connections}

            self.step(move, link_capacity)
            nb_turn += 1
            print(" ".join(move))
        print(f"\nTotal turns: {nb_turn}")

    def step(self, move: list[str], link_capacity: dict[Connection, int]
             ) -> None:
        """
        """
        for drone in self.all_drone:
            if drone.current_zone == self.graph.end_hub:
                continue

            current_zone = self.graph.retrieve_zone_by_name(drone.current_zone)
            neighbours = self.graph.retrieve_neighbour(current_zone)
            neighbours = sorted(neighbours, key=lambda n: (n.weight,
                                                           n.zone != "priority"
                                                           ))
            if drone.next_hub:
                current_connection = (
                    self.graph.retrieve_connection_by_zones([drone.next_hub,
                                                                current_zone])
                                                                )

                drone.next_hub.in_link.remove(drone)
                drone.next_hub.current_occupancy.append(drone)
                drone.current_zone = drone.next_hub.name
                link_capacity[current_connection] -= 1
                move.append(f"D{drone.id}-{drone.current_zone}")
                drone.next_hub = None
                continue
            for next_hub in neighbours:
                if next_hub.weight < current_zone.weight:
                    current_connection = (
                        self.graph.retrieve_connection_by_zones([next_hub,
                                                                 current_zone])
                                                                 )

                    if (next_hub.zone == "restricted"
                        and link_capacity[current_connection] > 0
                            and drone not in next_hub.in_link):
                        if next_hub.restricted_link_checking():
                            next_hub.in_link.append(drone)
                            current_zone.current_occupancy.remove(drone)
                            drone.next_hub = next_hub
                            link_capacity[current_connection] -= 1
                            move.append(f"D{drone.id}-"
                                        f"{current_connection.zones[0].name}-"
                                        f"{current_connection.zones[1].name}")
                            break
                    elif ((next_hub.capacity_checking()
                           or next_hub.name == self.graph.end_hub)
                            and link_capacity[current_connection] > 0):
                        next_hub.current_occupancy.append(drone)
                        drone.current_zone = next_hub.name
                        current_zone.current_occupancy.remove(drone)
                        move.append(f"D{drone.id}-{drone.current_zone}")
                        if drone in next_hub.in_link:
                            next_hub.in_link.remove(drone)
                        link_capacity[current_connection] -= 1
                        break
                else:
                    break
