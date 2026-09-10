import time
import pygame as py
from pygame import Surface
from .zone import Zone
from .simulation import Simulation
from .drone import Drone


class Visualisation:
    """
    """
    def __init__(self, simulation: Simulation, window: Surface, window_width: int, window_height: int):
        self.simulation = simulation
        self.window = window
        self.window_width = window_width
        self.window_height = window_height

    def draw_hub(self, hub: Zone, image: Surface, scroll_x: int, scroll_y: int):
        """
        """
        tile_size = image.get_width()

        origin_x = self.window_width // 2
        origin_y = self.window_height // 2

        screen_x = (origin_x + hub.x * tile_size - scroll_x)
        screen_y = (origin_y + hub.y * tile_size - scroll_y)

        self.window.blit(image, (screen_x, screen_y))

    def draw_hubs(self, image: Surface, scroll_x: int, scroll_y: int):
        """
        """
        for hub in self.simulation.graph.zones:
            self.draw_hub(hub, image, scroll_x, scroll_y)

    def draw_connection(self, image: Surface, zones: list[Zone], scroll_x: int, scroll_y: int) -> None:
        """
        """
        tile_size = image.get_width()
        
        origin_x = self.window_width // 2
        origin_y = self.window_height // 2

        start_x = (origin_x + zones[0].x * tile_size - scroll_x) + 100
        start_y = (origin_y + zones[0].y * tile_size - scroll_y) + 100

        end_x = (origin_x + zones[1].x * tile_size - scroll_x) + 100
        end_y = (origin_y + zones[1].y * tile_size - scroll_y) + 100

        py.draw.line(self.window, "white", (start_x, start_y), (end_x, end_y), 1)

    def draw_connections(self, image: Surface , scroll_x: int, scroll_y: int) -> None:
        """
        """
        for connection in self.simulation.graph.connections:
            self.draw_connection(image, connection.zones, scroll_x, scroll_y)

    def draw_drone(self, drone: Drone, drone_img, scroll_x, scroll_y, image: Surface) -> None:
        """
        """
        tile_size = image.get_width()

        origin_x = self.window_width // 2
        origin_y = self.window_height // 2
        hub = self.simulation.graph.retrieve_zone_by_name(drone.current_zone)

        index = hub.current_occupancy.index(drone)
        screen_x = (origin_x + hub.x * tile_size - scroll_x) + 100 - (index % 5) * 15
        screen_y = (origin_y + hub.y * tile_size - scroll_y) + 100 - (index // 5) * 30

        self.window.blit(drone_img, (screen_x, screen_y))

    def draw_drones(self, drone_img: Surface, scroll_x: int, scroll_y: int, image: Surface) -> None:
        """
        """
        for drone in self.simulation.all_drone:
            self.draw_drone(drone, drone_img, scroll_x, scroll_y, image)

    def visualizer(self) -> None:
        """
        """
        WORLD_WIDTH = 10**4
        WORLD_HEIGHT = 10**4

        BAR_SIZE = 15

        scroll_x = 0
        scroll_y = 0

        dragging_vertical = False
        dragging_horizontal = False

        cursor_offset_y = 0
        cursor_offset_x = 0

        running = True
        nb_turn = 0

        end_zone = (self.simulation.graph.retrieve_zone_by_name(self.simulation.graph.end_hub))

        fond = py.image.load("fond.jpg")
        hub_image = py.image.load("hub.png")
        hub_image = py.transform.scale(hub_image,(200, 200))
        drone_img = py.image.load("star_wars.png")
        drone_img = py.transform.scale(drone_img, (50, 50))

        last_step_time = py.time.get_ticks()
        while running:
            current_time = py.time.get_ticks()
            scrollbar_vertical = py.Rect(self.window_width - BAR_SIZE, 0,
                BAR_SIZE, self.window_height - BAR_SIZE)

            max_scroll_y = max(0, WORLD_HEIGHT - self.window_height)

            ratio_y = min(
                1,
                self.window_height / WORLD_HEIGHT
            )

            cursor_height = max(30,int(scrollbar_vertical.height* ratio_y))

            max_cursor_y = max(0,scrollbar_vertical.height - cursor_height)

            if max_scroll_y > 0:
                cursor_y = int((scroll_y / max_scroll_y) * max_cursor_y)
            else:
                cursor_y = 0

            cursor_vertical = py.Rect(self.window_width - BAR_SIZE, cursor_y,
                BAR_SIZE,cursor_height)

            scrollbar_horizontal = py.Rect(0, self.window_height - BAR_SIZE,
                self.window_width - BAR_SIZE, BAR_SIZE)

            max_scroll_x = max(0, WORLD_WIDTH - self.window_width)

            ratio_x = min(1, self.window_width / WORLD_WIDTH)

            cursor_width = max(30, int(scrollbar_horizontal.width * ratio_x))

            max_cursor_x = max(0, scrollbar_horizontal.width - cursor_width)

            if max_scroll_x > 0:
                cursor_x = int((scroll_x / max_scroll_x) * max_cursor_x)
            else:
                cursor_x = 0

            cursor_horizontal = py.Rect(cursor_x,
                self.window_height - BAR_SIZE, cursor_width, BAR_SIZE)
            for event in py.event.get():
                if event.type == py.QUIT:
                    running = False
                elif event.type == py.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if cursor_vertical.collidepoint(event.pos):
                            dragging_vertical = True

                            cursor_offset_y = (event.pos[1] 
                            - cursor_vertical.y)
                        elif cursor_horizontal.collidepoint(event.pos):
                            dragging_horizontal = True

                            cursor_offset_x = (event.pos[0]
                                               - cursor_horizontal.x)
                elif event.type == py.MOUSEBUTTONUP:
                    if event.button == 1:
                        dragging_vertical = False
                        dragging_horizontal = False

                elif event.type == py.MOUSEMOTION:
                    if dragging_vertical:
                        mouse_y = event.pos[1]

                        new_cursor_y = (mouse_y - cursor_offset_y)
                        new_cursor_y = max(0, min(new_cursor_y, max_cursor_y))

                        if max_cursor_y > 0:
                            scroll_y = int((new_cursor_y / max_cursor_y)
                                           * max_scroll_y)
                    if dragging_horizontal:
                        mouse_x = event.pos[0]
                        new_cursor_x = (mouse_x - cursor_offset_x)
                        new_cursor_x = max(0, min(new_cursor_x, max_cursor_x))

                        if max_cursor_x > 0:
                            scroll_x = int((new_cursor_x / max_cursor_x)
                                * max_scroll_x)
            scroll_x = max(0, min(scroll_x, max_scroll_x))
            scroll_y = max(0, min(scroll_y, max_scroll_y))

            if (current_time - last_step_time >= 1000 and len(end_zone.current_occupancy) < self.simulation.graph.nb_drone):

                move: list[str] = []

                link_capacity = {
                    connection: connection.max_link_capacity
                    for connection
                    in self.simulation.graph.connections
                }

                self.simulation.step(move, link_capacity)
                nb_turn += 1

                print(" ".join(move))
                last_step_time = py.time.get_ticks()

            self.window.fill((0, 0, 0))

            # self.window.blit(fond, (-scroll_x, -scroll_y))
            self.draw_hubs(hub_image, scroll_x, scroll_y)
            self.draw_connections(hub_image, scroll_x, scroll_y)
            self.draw_drones(drone_img, scroll_x, scroll_y, hub_image)

            if max_scroll_y > 0:
                cursor_y = int((scroll_y / max_scroll_y) * max_cursor_y)
            else:
                cursor_y = 0

            cursor_vertical.y = cursor_y

            if max_scroll_x > 0:
                cursor_x = int((scroll_x / max_scroll_x) * max_cursor_x)
            else:
                cursor_x = 0

            cursor_horizontal.x = cursor_x

            py.draw.rect(self.window, (40, 40, 40), scrollbar_vertical)
            py.draw.rect(self.window, (150, 150, 150), cursor_vertical)
            py.draw.rect(self.window, (40, 40, 40), scrollbar_horizontal)
            py.draw.rect(self.window, (150, 150, 150), cursor_horizontal)

            py.display.flip()

        print(f"\nTotal turns: {nb_turn}")
