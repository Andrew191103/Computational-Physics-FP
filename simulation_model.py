import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class SimulationModel:
    def __init__(self):
        self.cart_position = 0
        self.cart_velocity = 0
        self.net_force = 0
        self.left_force = 0
        self.right_force = 0
        self.mass = 1  # in kilograms
        self.time_step = 0.01  # time step for the simulation
        self.gravity = 9.81  # m/s^2, default Earth gravity
        self.friction_coefficient = 0.1  # default friction coefficient
        self.angle = 0  # default angle of the plane
        self.left_wall = 0  # position of the left wall
        self.right_wall = 100  # position of the right wall

    def update_forces(self, left_force, right_force):
        self.left_force = left_force
        self.right_force = right_force
        self.net_force = self.right_force - self.left_force
        logging.debug(f"Left Force: {self.left_force}, Right Force: {self.right_force}, Net Force: {self.net_force}")

    def update_environment(self, gravity, friction_coefficient, angle):
        self.gravity = gravity
        self.friction_coefficient = friction_coefficient
        self.angle = angle
        logging.debug(f"Gravity: {self.gravity}, Friction Coefficient: {self.friction_coefficient}, Angle: {self.angle}")

    def update_weight(self, weight):
        self.mass = weight
        logging.debug(f"Updated Weight: {self.mass}")

    def step(self):
        # Update the velocity and position of the cart using basic physics
        normal_force = self.mass * self.gravity * np.cos(np.radians(self.angle))
        friction_force = self.friction_coefficient * normal_force
        applied_force = self.net_force - friction_force * np.sign(self.cart_velocity)
        acceleration = (applied_force / self.mass) - self.gravity * np.sin(np.radians(self.angle))
        self.cart_velocity += acceleration * self.time_step
        self.cart_position += self.cart_velocity * self.time_step

        # Collision detection with walls
        if self.cart_position <= self.left_wall:
            self.cart_position = self.left_wall
            self.cart_velocity = 0
        elif self.cart_position >= self.right_wall:
            self.cart_position = self.right_wall
            self.cart_velocity = 0

        logging.debug(f"Position: {self.cart_position}, Velocity: {self.cart_velocity}, Acceleration: {acceleration}")

    def reset(self):
        self.cart_position = 0
        self.cart_velocity = 0
        self.net_force = 0
        self.left_force = 0
        self.right_force = 0
        logging.debug("Simulation reset.")
