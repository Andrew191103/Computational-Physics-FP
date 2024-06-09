import pygame
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class SimulationController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 800))
        self.font = pygame.font.SysFont(None, 36)

        # Sliders for left and right forces
        self.left_force_slider = pygame.Rect(50, 50, 200, 20)
        self.right_force_slider = pygame.Rect(950, 50, 200, 20)
        self.left_force = 0
        self.right_force = 0

        # Sliders for gravity, friction coefficient, angle, and weight
        self.gravity_slider = pygame.Rect(50, 300, 200, 20)
        self.friction_slider = pygame.Rect(50, 350, 200, 20)
        self.angle_slider = pygame.Rect(50, 400, 200, 20)
        self.weight_slider = pygame.Rect(50, 450, 200, 20)
        self.gravity = 9.81
        self.friction_coefficient = 0.1
        self.angle = 0
        self.weight = 1

    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        if mouse_pressed[0]:
            if self.left_force_slider.collidepoint(mouse_pos):
                self.left_force = (mouse_pos[0] - self.left_force_slider.x) / self.left_force_slider.width * 100
                self.model.update_forces(self.left_force, self.right_force)
            elif self.right_force_slider.collidepoint(mouse_pos):
                self.right_force = (mouse_pos[0] - self.right_force_slider.x) / self.right_force_slider.width * 100
                self.model.update_forces(self.left_force, self.right_force)
            elif self.gravity_slider.collidepoint(mouse_pos):
                self.gravity = (mouse_pos[0] - self.gravity_slider.x) / self.gravity_slider.width * 20
                self.model.update_environment(self.gravity, self.friction_coefficient, self.angle)
            elif self.friction_slider.collidepoint(mouse_pos):
                self.friction_coefficient = (mouse_pos[0] - self.friction_slider.x) / self.friction_slider.width
                self.model.update_environment(self.gravity, self.friction_coefficient, self.angle)
            elif self.angle_slider.collidepoint(mouse_pos):
                self.angle = (mouse_pos[0] - self.angle_slider.x) / self.angle_slider.width * 90
                self.model.update_environment(self.gravity, self.friction_coefficient, self.angle)
            elif self.weight_slider.collidepoint(mouse_pos):
                self.weight = (mouse_pos[0] - self.weight_slider.x) / self.weight_slider.width * 50
                self.model.update_weight(self.weight)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.model.reset()

        return True

    def draw_ui(self):
        pygame.draw.rect(self.screen, (100, 100, 100), self.left_force_slider)
        pygame.draw.rect(self.screen, (100, 100, 100), self.right_force_slider)
        pygame.draw.rect(self.screen, (100, 100, 100), self.gravity_slider)
        pygame.draw.rect(self.screen, (100, 100, 100), self.friction_slider)
        pygame.draw.rect(self.screen, (100, 100, 100), self.angle_slider)
        pygame.draw.rect(self.screen, (100, 100, 100), self.weight_slider)

        pygame.draw.rect(self.screen, (0, 0, 255), (self.left_force_slider.x, self.left_force_slider.y, self.left_force_slider.width * (self.left_force / 100), self.left_force_slider.height))
        pygame.draw.rect(self.screen, (255, 0, 0), (self.right_force_slider.x, self.right_force_slider.y, self.right_force_slider.width * (self.right_force / 100), self.right_force_slider.height))
        pygame.draw.rect(self.screen, (0, 255, 0), (self.gravity_slider.x, self.gravity_slider.y, self.gravity_slider.width * (self.gravity / 20), self.gravity_slider.height))
        pygame.draw.rect(self.screen, (255, 255, 0), (self.friction_slider.x, self.friction_slider.y, self.friction_slider.width * (self.friction_coefficient / 1), self.friction_slider.height))
        pygame.draw.rect(self.screen, (0, 255, 255), (self.angle_slider.x, self.angle_slider.y, self.angle_slider.width * (self.angle / 90), self.angle_slider.height))
        pygame.draw.rect(self.screen, (255, 0, 255), (self.weight_slider.x, self.weight_slider.y, self.weight_slider.width * (self.weight / 50), self.weight_slider.height))

        left_force_text = self.font.render(f"Left Force: {self.left_force:.2f}", True, (0, 0, 0))
        right_force_text = self.font.render(f"Right Force: {self.right_force:.2f}", True, (0, 0, 0))
        net_force_text = self.font.render(f"Net Force: {self.model.net_force:.2f}", True, (0, 0, 0))
        velocity_text = self.font.render(f"Velocity: {self.model.cart_velocity:.2f}", True, (0, 0, 0))
        position_text = self.font.render(f"Position: {self.model.cart_position:.2f}", True, (0, 0, 0))
        gravity_text = self.font.render(f"Gravity: {self.gravity:.2f}", True, (0, 0, 0))
        friction_text = self.font.render(f"Friction: {self.friction_coefficient:.2f}", True, (0, 0, 0))
        angle_text = self.font.render(f"Angle: {self.angle:.2f}", True, (0, 0, 0))
        weight_text = self.font.render(f"Weight: {self.weight:.2f}", True, (0, 0, 0))

        self.screen.blit(left_force_text, (50, 20))
        self.screen.blit(right_force_text, (950, 20))
        self.screen.blit(net_force_text, (500, 20))
        self.screen.blit(velocity_text, (500, 50))
        self.screen.blit(position_text, (500, 80))
        self.screen.blit(gravity_text, (50, 270))
        self.screen.blit(friction_text, (50, 320))
        self.screen.blit(angle_text, (50, 370))
        self.screen.blit(weight_text, (50, 420))

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.view.run()
            self.draw_ui()
            pygame.display.flip()
            logging.debug("UI updated.")
