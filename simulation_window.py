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
        SimulationWindow (base class/template): Defines the skeleton of the simulation 
        UI algorithm in its init_ui() method. Declares abstract placeholder 
        methods to be implemented by subclasses:
            - create_input_group()
            - create_result_group()
            - update_units()
            - reset_to_default()
            - start_simulation()
            - calculate() (implied by its use in init_ui())
    
        CarCollisionWindow, DroneInterceptWindow (subclasses/implementation): 
        Implements the abstract methods defined in SimulationWindow.
        Provides specific behavior for both simulations.
"""


class SimulationWindow(QWidget):
    """
    Base class for simulation windows.
    """

    # Log initialization
    logging.info("SimulationWindow initialized")

    def __init__(self, config) -> None:
        """
        Initializes the simulation window.
        """
        super().__init__()
        self.config = config
        self.init_ui()

    def init_ui(self) -> None:
        """
        Initializes the user interface of the simulation window.
        """
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Input fields group
        self.create_input_group(layout)

        # Problem group
        self.create_problem_group(layout)

        # Result label group
        self.create_result_group(layout)

        # Chart setup
        self.chart_view = QChartView()
        layout.addWidget(self.chart_view)

        # Calculate outcome
        self.calculate()

        # Reset button
        reset_button = QPushButton("Reset to Default")
        reset_button.clicked.connect(self.reset_to_default)
        layout.addWidget(reset_button)

        # Simulation button
        self.start_simulation_button = QPushButton("Start Simulation")
        self.start_simulation_button.clicked.connect(self.start_simulation)
        layout.addWidget(self.start_simulation_button)

    def create_input_group(self) -> None:
        """
        Placeholder method to be implemented by subclasses.
        Creates the input group box with widgets for simulation parameters.

        Raises:
            NotImplementedError: This method must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement create_input_group")

    def create_problem_group(self) -> None:
        """
        Creates the problem group box with a description of the simulation.

        Raises:
            NotImplementedError: This method must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement create_problem_group")

    def create_result_group(self) -> None:
        """
        Placeholder method to be implemented by subclasses.
        Creates the result group box to display the calculated results.

        Raises:
            NotImplementedError: This method must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement create_result_group")

    def update_units(self) -> None:
        """
        Placeholder method to be implemented by subclasses.
        Handles unit changes and updates the calculations accordingly.

        Raises:
            NotImplementedError: This method must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement update_units")

    def reset_to_default(self) -> None:
        """
        Placeholder method to be implemented by subclasses.
        Resets the input fields to their default values.

        Raises:
            NotImplementedError: This method must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement reset_to_default")

    def start_simulation(self) -> None:
        """
        Placeholder method to be implemented by subclasses.
        Starts the dynamic simulation in a separate window.

        Raises:
            NotImplementedError: This method must be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement start_simulation")

    def validate_input(self, value, min_value=None, max_value=None) -> bool:
        """
        Validates an input value against specified minimum and maximum values.

        Parameters:
            value: The input value to validate.
            min_value: The minimum allowed value (optional).
            max_value: The maximum allowed value (optional).

        Returns:
            bool: True if the value is valid, False otherwise.
        """
        if min_value is not None and value < min_value:
            return False
        if max_value is not None and value > max_value:
            return False
        return True
