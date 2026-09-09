import pygame as py
from pygame import Surface
from .zone import Zone
from .simulation import Simulation


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

        origin_y = self.window_height // 2

        screen_x = (hub.x * tile_size - scroll_x)
        screen_y = (origin_y + hub.y * tile_size - scroll_y)

        self.window.blit(image, (screen_x, screen_y))

    def draw_hubs(self, image: Surface, scroll_x: int, scroll_y: int):
        """
        """
        for hub in self.simulation.graph.zones:
            self.draw_hub(hub, image, scroll_x, scroll_y)

    def visualizer(self) -> None:
        """
        """
        WORLD_WIDTH = 1600
        WORLD_HEIGHT = 1000

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
        hub_image = py.transform.scale(hub_image,(250, 250))

        while running:
            scrollbar_vertical = py.Rect(
                self.window_width - BAR_SIZE,
                0,
                BAR_SIZE,
                self.window_height - BAR_SIZE
            )

            max_scroll_y = max(
                0,
                WORLD_HEIGHT - self.window_height
            )

            ratio_y = min(
                1,
                self.window_height / WORLD_HEIGHT
            )

            cursor_height = max(
                30,
                int(
                    scrollbar_vertical.height
                    * ratio_y
                )
            )

            max_cursor_y = max(
                0,
                scrollbar_vertical.height
                - cursor_height
            )

            if max_scroll_y > 0:
                cursor_y = int(
                    (
                        scroll_y
                        / max_scroll_y
                    )
                    * max_cursor_y
                )
            else:
                cursor_y = 0

            cursor_vertical = py.Rect(
                self.window_width - BAR_SIZE,
                cursor_y,
                BAR_SIZE,
                cursor_height
            )

            scrollbar_horizontal = py.Rect(
                0,
                self.window_height - BAR_SIZE,
                self.window_width - BAR_SIZE,
                BAR_SIZE
            )

            max_scroll_x = max(
                0,
                WORLD_WIDTH - self.window_width
            )

            ratio_x = min(
                1,
                self.window_width / WORLD_WIDTH
            )

            cursor_width = max(
                30,
                int(
                    scrollbar_horizontal.width
                    * ratio_x
                )
            )

            max_cursor_x = max(
                0,
                scrollbar_horizontal.width
                - cursor_width
            )

            if max_scroll_x > 0:
                cursor_x = int(
                    (
                        scroll_x
                        / max_scroll_x
                    )
                    * max_cursor_x
                )
            else:
                cursor_x = 0

            cursor_horizontal = py.Rect(
                cursor_x,
                self.window_height - BAR_SIZE,
                cursor_width,
                BAR_SIZE
            )

            # ======================================
            # EVENEMENTS
            # ======================================

            for event in py.event.get():

                # -------------------------------
                # FERMETURE
                # -------------------------------

                if event.type == py.QUIT:
                    running = False

                # -------------------------------
                # MOLETTE
                # -------------------------------

                elif event.type == py.MOUSEWHEEL:

                    scroll_y -= event.y * 50

                # -------------------------------
                # CLIC SOURIS
                # -------------------------------

                elif event.type == py.MOUSEBUTTONDOWN:

                    if event.button == 1:

                        # Scrollbar verticale
                        if cursor_vertical.collidepoint(
                            event.pos
                        ):
                            dragging_vertical = True

                            cursor_offset_y = (
                                event.pos[1]
                                - cursor_vertical.y
                            )

                        # Scrollbar horizontale
                        elif cursor_horizontal.collidepoint(
                            event.pos
                        ):
                            dragging_horizontal = True

                            cursor_offset_x = (
                                event.pos[0]
                                - cursor_horizontal.x
                            )

                # -------------------------------
                # RELACHEMENT SOURIS
                # -------------------------------

                elif event.type == py.MOUSEBUTTONUP:

                    if event.button == 1:
                        dragging_vertical = False
                        dragging_horizontal = False

                # -------------------------------
                # DEPLACEMENT SOURIS
                # -------------------------------

                elif event.type == py.MOUSEMOTION:

                    # ===========================
                    # SCROLL VERTICAL
                    # ===========================

                    if dragging_vertical:

                        mouse_y = event.pos[1]

                        new_cursor_y = (
                            mouse_y
                            - cursor_offset_y
                        )

                        new_cursor_y = max(
                            0,
                            min(
                                new_cursor_y,
                                max_cursor_y
                            )
                        )

                        if max_cursor_y > 0:
                            scroll_y = int(
                                (
                                    new_cursor_y
                                    / max_cursor_y
                                )
                                * max_scroll_y
                            )

                    # ===========================
                    # SCROLL HORIZONTAL
                    # ===========================

                    if dragging_horizontal:

                        mouse_x = event.pos[0]

                        new_cursor_x = (
                            mouse_x
                            - cursor_offset_x
                        )

                        new_cursor_x = max(
                            0,
                            min(
                                new_cursor_x,
                                max_cursor_x
                            )
                        )

                        if max_cursor_x > 0:
                            scroll_x = int(
                                (
                                    new_cursor_x
                                    / max_cursor_x
                                )
                                * max_scroll_x
                            )

            # ======================================
            # LIMITES DU SCROLL
            # ======================================

            scroll_x = max(
                0,
                min(
                    scroll_x,
                    max_scroll_x
                )
            )

            scroll_y = max(
                0,
                min(
                    scroll_y,
                    max_scroll_y
                )
            )

            # ======================================
            # SIMULATION
            # ======================================

            while (
                len(end_zone.current_occupancy)
                < self.simulation.graph.nb_drone
            ):

                move: list[str] = []

                link_capacity = {
                    connection: connection.max_link_capacity
                    for connection
                    in self.simulation.graph.connections
                }

                self.simulation.step(
                    move,
                    link_capacity
                )

                nb_turn += 1

                print(" ".join(move))

            # ======================================
            # AFFICHAGE
            # ======================================

            self.window.fill((0, 0, 0))

            # Fond
            self.window.blit(
                fond,
                (-scroll_x, -scroll_y)
            )

            # Hubs
            self.draw_hubs(
                hub_image,
                scroll_x,
                scroll_y
            )

            # ======================================
            # RECALCUL POSITION CURSEUR
            # ======================================

            if max_scroll_y > 0:
                cursor_y = int(
                    (
                        scroll_y
                        / max_scroll_y
                    )
                    * max_cursor_y
                )
            else:
                cursor_y = 0

            cursor_vertical.y = cursor_y

            if max_scroll_x > 0:
                cursor_x = int(
                    (
                        scroll_x
                        / max_scroll_x
                    )
                    * max_cursor_x
                )
            else:
                cursor_x = 0

            cursor_horizontal.x = cursor_x

            # ======================================
            # SCROLLBAR VERTICALE
            # ======================================

            py.draw.rect(
                self.window,
                (40, 40, 40),
                scrollbar_vertical
            )

            py.draw.rect(
                self.window,
                (150, 150, 150),
                cursor_vertical
            )

            # ======================================
            # SCROLLBAR HORIZONTALE
            # ======================================

            py.draw.rect(
                self.window,
                (40, 40, 40),
                scrollbar_horizontal
            )

            py.draw.rect(
                self.window,
                (150, 150, 150),
                cursor_horizontal
            )

            # ======================================
            # AFFICHAGE
            # ======================================

            py.display.flip()

        print(f"\nTotal turns: {nb_turn}")
