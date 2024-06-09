from simulation_model import SimulationModel
from simulation_view import SimulationView
from simulation_controller import SimulationController

if __name__ == "__main__":
    model = SimulationModel()
    view = SimulationView(model)
    controller = SimulationController(model, view)
    controller.run()
