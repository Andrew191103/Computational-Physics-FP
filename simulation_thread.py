import threading
import time
import queue

class SimulationThread(threading.Thread):
    def __init__(self, simulation_queue):
        super().__init__()
        self.simulation_queue = simulation_queue
        self.running = True

    def run(self):
        while self.running:
            # Simulate your physics or other calculations here
            result = self.simulate()
            
            # Put the result into the queue to communicate with the GUI
            self.simulation_queue.put(result)
            
            # Sleep to limit the simulation update rate (e.g., 60 updates per second)
            time.sleep(1/60)

    def simulate(self):
        # Replace this with your actual simulation code
        # For example, updating the cart's position and velocity
        # Dummy simulation result
        return {
            'position': (100, 200),
            'velocity': (5, 10)
        }

    def stop(self):
        self.running = False
