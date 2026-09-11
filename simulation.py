from graph import Graph
from drone import Drone
from connection import Connection


class Simulation:
    """
    Manages and runs the drone simulation on a graph.

    The simulation creates the configured number of drones, places them in
    the starting hub, and moves them through the graph until all drones reach
    the destination hub.

    Attributes:
        graph (Graph): The graph containing the zones, connections, and
            simulation configuration.
        all_drone (list[Drone]): The list of drones participating in the
            simulation.
    """
    def __init__(self, graph: Graph) -> None:
        """
        Initialize a simulation with the given graph.

        Creates the configured number of drones, places them in the starting
        hub, and initializes their current zones.

        Args:
            graph (Graph): The graph on which the simulation will run.
        """
        self.graph: Graph = graph
        all_drone: list[Drone] = []
        for i in range(0, graph.nb_drone):
            drone = Drone(i + 1, graph.start_hub)
            all_drone.append(drone)
        zone = graph.retrieve_zone_by_name(graph.start_hub)
        if zone:
            for drone in all_drone:
                self.drone = drone
                zone.current_occupancy.append(drone)
                drone.current_zone = zone.name
            self.all_drone = all_drone

    def simulate(self) -> None:
        """
        Run the simulation until all drones reach the destination hub.

        The simulation advances one turn at a time, tracking the available
        capacity of each connection and recording the movements of each
        drone. The total number of turns is printed when the simulation ends.
        """
        nb_turn = 0
        end_zone = self.graph.retrieve_zone_by_name(self.graph.end_hub)

        if end_zone:
            while len(end_zone.current_occupancy) < self.graph.nb_drone:
                move: list[str] = []
                link_capacity = {
                    connection: connection.max_link_capacity
                    for connection in self.graph.connections
                }

                self.step(move, link_capacity)
                nb_turn += 1
                print(" ".join(move))
            print(f"\nTotal turns: {nb_turn}")

    def step(self, move: list[str], link_capacity: dict[Connection, int]
             ) -> None:
        """
        Execute one simulation turn.

        Each drone is evaluated and moved to a neighbouring zone when
        possible. Movement is determined by zone weights, zone capacity,
        connection capacity, and restrictions. Drones entering restricted
        zones may require an additional turn before completing the movement.

        Args:
            move (list[str]): List that is populated with the movements
                performed during the current turn.
            link_capacity (dict[Connection, int]): Remaining capacity of
                each connection for the current turn.
        """
        for drone in self.all_drone:
            if drone.current_zone == self.graph.end_hub:
                continue

            current_zone = self.graph.retrieve_zone_by_name(drone.current_zone)
            if current_zone is None:
                return
            neighbours = self.graph.retrieve_neighbour(current_zone)
            neighbours = sorted(neighbours, key=lambda n: (n.weight,
                                                           n.zone != "priority"
                                                           ))
            if current_zone:
                if drone.next_hub:
                    current_connection = (
                        self.graph.retrieve_connection_by_zones(
                            [drone.next_hub, current_zone]))

                    drone.next_hub.in_link.remove(drone)
                    drone.next_hub.current_occupancy.append(drone)
                    drone.current_zone = drone.next_hub.name
                    if current_connection is None:
                        return
                    link_capacity[current_connection] -= 1
                    move.append(f"D{drone.id}-{drone.current_zone}")
                    drone.next_hub = None
                    continue
                for next_hub in neighbours:
                    if next_hub.weight < current_zone.weight:
                        current_connection = (
                            self.graph.retrieve_connection_by_zones(
                                [next_hub, current_zone]))

                        if current_connection:
                            if (next_hub.zone == "restricted"
                                and link_capacity[current_connection] > 0
                                    and drone not in next_hub.in_link):
                                if next_hub.restricted_link_checking():
                                    next_hub.in_link.append(drone)
                                    current_zone.current_occupancy.remove(
                                        drone)
                                    drone.next_hub = next_hub
                                    link_capacity[current_connection] -= 1
                                    move.append(
                                        f"D{drone.id}- \
                                            {current_connection.zones[0].name}"
                                        f"-{current_connection.zones[1].name}"
                                    )

                                    break
                            elif (
                                (next_hub.capacity_checking()
                                    or next_hub.name == self.graph.end_hub)
                                    and link_capacity[current_connection] > 0
                                    ):
                                next_hub.current_occupancy.append(drone)
                                drone.current_zone = next_hub.name
                                current_zone.current_occupancy.remove(drone)
                                move.append(f"D{drone.id}-{drone.current_zone}"
                                            )
                                if drone in next_hub.in_link:
                                    next_hub.in_link.remove(drone)
                                link_capacity[current_connection] -= 1
                                break
                        else:
                            break
