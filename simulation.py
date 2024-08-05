from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PySide6.QtCharts import QChartView
import logging

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s",
)

"""
Design Pattern:
    Template Method Pattern:
        Simulation (base class/template): Defines the skeleton of the simulation 
        UI algorithm in its init_ui() method. Declares abstract placeholder 
        methods to be implemented by subclasses:
            - init_ui()
            - init_chart()
            - update_simulation()
    
        CarCollisionSimulation, DroneInterceptSimulation (subclasses/implementation): 
        Implements the abstract methods defined in Simulation.
        Provides specific behavior for both simulations.
"""


class Simulation(QWidget):
    """
    Base class for simulation windows.
    """

    # Log initialization
    logging.info("Simulation initialized")

    def __init__(self, problem, *args):
        super().__init__()
        if problem == "car":
            speed_car_a, speed_car_b, initial_distance = args
            self.speed_car_a = speed_car_a
            self.speed_car_b = speed_car_b
            self.initial_distance = initial_distance
            self.time = 0
        elif problem == "drone":
            drone_speed, radar_range, reaction_time = args
            self.drone_speed = drone_speed
            self.radar_range = radar_range
            self.reaction_time = reaction_time
            self.time = -reaction_time
            self.starting_y = self.radar_range + (
                (self.drone_speed / 60) * abs(self.time)
            )
        else:
            raise ValueError("Invalid window type")

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.init_chart()

        self.update_simulation()

    def init_chart(self):
        """
        Placeholder method to be implemented by subclasses.
        Initializes the chart.

        Raises:
            NotImplementedError: This method must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement init_chart")

    def update_simulation(self):
        """
        Placeholder method to be implemented by subclasses.
        Updates the simulation.

        Raises:
            NotImplementedError: This method must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement update_simulation")
