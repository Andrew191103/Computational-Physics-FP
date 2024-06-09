import pygame
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class SimulationView:
    def __init__(self, model):
        self.model = model
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 800))
        self.clock = pygame.time.Clock()

        self.fig, self.ax = plt.subplots(figsize=(8, 2))
        self.canvas = FigureCanvas(self.fig)

        self.positions = []
        self.velocities = []

    def draw(self):
        self.screen.fill((255, 255, 255))

        # Draw walls
        left_wall_x = 200
        right_wall_x = 1000
        base_y = 500
        pygame.draw.line(self.screen, (0, 0, 0), (left_wall_x, base_y), (left_wall_x, base_y - 200), 5)

        # Draw incline surface
        incline_angle_rad = np.radians(self.model.angle)
        incline_length = right_wall_x - left_wall_x
        base_x = left_wall_x
        top_x = base_x + incline_length * np.cos(incline_angle_rad)
        top_y = base_y - incline_length * np.sin(incline_angle_rad)
        pygame.draw.line(self.screen, (0, 0, 0), (base_x, base_y), (top_x, top_y), 5)

        # Draw the right wall following the incline
        pygame.draw.line(self.screen, (0, 0, 0), (top_x, top_y), (top_x, top_y - 200), 5)

        # Draw cart
        cart_x = base_x + int(self.model.cart_position * 10 * np.cos(incline_angle_rad))
        cart_y = base_y - int(self.model.cart_position * 10 * np.sin(incline_angle_rad)) - 10
        pygame.draw.rect(self.screen, (0, 0, 0), (cart_x - 10, cart_y, 20, 20))

        # Normalize force values for arrow lengths
        max_arrow_length = 100
        max_force_display = 100  # Max force value to display without scaling
        left_arrow_length = min(abs(self.model.left_force), max_force_display) / max_force_display * max_arrow_length
        right_arrow_length = min(abs(self.model.right_force), max_force_display) / max_force_display * max_arrow_length

        # Draw force arrows
        pygame.draw.line(self.screen, (0, 0, 255), (cart_x, cart_y + 10), (cart_x - left_arrow_length, cart_y + 10), 5)
        pygame.draw.line(self.screen, (255, 0, 0), (cart_x, cart_y + 10), (cart_x + right_arrow_length, cart_y + 10), 5)

        # Update and draw graphs
        self.positions.append(self.model.cart_position)
        self.velocities.append(self.model.cart_velocity)

        # Limit the size of the lists to avoid memory issues
        if len(self.positions) > 100:
            self.positions.pop(0)
        if len(self.velocities) > 100:
            self.velocities.pop(0)

        self.ax.clear()
        self.ax.plot(self.positions, label='Position', color='blue')
        self.ax.plot(self.velocities, label='Velocity', color='red')
        self.ax.legend()

        # Set y-limits with a minimum range
        min_y = min(min(self.positions), min(self.velocities))
        max_y = max(max(self.positions), max(self.velocities))
        if min_y == max_y:
            min_y -= 0.1
            max_y += 0.1
        self.ax.set_ylim(min_y, max_y)

        self.canvas.draw()
        graph_surface = pygame.image.fromstring(self.canvas.tostring_rgb(), self.canvas.get_width_height(), "RGB")
        graph_surface = pygame.transform.scale(graph_surface, (1000, 200))
        self.screen.blit(graph_surface, (100, 600))

    def run(self):
        self.model.step()
        self.draw()
        self.clock.tick(60)
        logging.debug(f"Cart Position: {self.model.cart_position}, Cart Velocity: {self.model.cart_velocity}")
