from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PySide6.QtCharts import QChartView

class SimulationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Input fields group
        self.create_input_group(layout)

        # Result label group
        self.create_result_group(layout)

        # Chart
        self.chart_view = QChartView()
        layout.addWidget(self.chart_view)

        self.calculate()
        
        # Reset button
        reset_button = QPushButton("Reset to Default")
        reset_button.clicked.connect(self.reset_to_default)
        layout.addWidget(reset_button)

        # Simulation button (to be implemented in subclasses)
        self.start_simulation_button = QPushButton("Start Simulation")
        self.start_simulation_button.clicked.connect(self.start_simulation)
        layout.addWidget(self.start_simulation_button)

    def create_input_group(self, layout):
        raise NotImplementedError("Subclasses must implement create_input_group")

    def create_result_group(self, layout):
        raise NotImplementedError("Subclasses must implement create_result_group")

    def update_units(self):
        raise NotImplementedError("Subclasses must implement update_units")

    def reset_to_default(self):
        raise NotImplementedError("Subclasses must implement reset_to_default")

    def start_simulation(self):
        raise NotImplementedError("Subclasses must implement start_simulation")

    def validate_input(self, value, min_value=None, max_value=None):
        if min_value is not None and value < min_value:
            return False
        if max_value is not None and value > max_value:
            return False
        return True
