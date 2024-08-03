from PySide6.QtWidgets import (
    QVBoxLayout,
    QMessageBox,
    QLabel,
    QDoubleSpinBox,
    QComboBox,
    QGroupBox,
    QFormLayout,
)
from PySide6.QtCharts import QChart, QLineSeries, QValueAxis, QScatterSeries
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPen
from unit_converter import UnitConverter
from simulation_window import SimulationWindow
from drone_intercept_simulation import DroneInterceptSimulation
import logging

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s",
)

"""
Design Patterns:
    Template Method: Inherits from SimulationWindow and implements methods.
"""


class DroneInterceptWindow(SimulationWindow):
    # Log initialization
    logging.info("DroneInterceptWindow initialized")

    def __init__(self):
        """
        Initialize the window
        """
        super().__init__()

    def create_input_group(self, layout):
        """
        Create the input group with input fields for drone speed, radar range, and reaction time

        Parameters:
            layout (QVBoxLayout): The layout to add the input group box to.
        """
        # Input fields
        self.drone_speed = QDoubleSpinBox()
        self.drone_speed.setRange(1.0, 999999.0)

        self.radar_range = QDoubleSpinBox()
        self.radar_range.setRange(1.0, 999999.0)

        self.reaction_time = QDoubleSpinBox()
        self.reaction_time.setRange(0.0, 999999.0)

        self.speed_unit_combo = QComboBox()
        self.speed_unit_combo.addItems(
            [
                "mph",
                "km/h",
                "m/h",
                "yd/h",
                "ft/h",
                "mpm",
                "km/min",
                "m/min",
                "yd/min",
                "ft/min",
                "mps",
                "km/s",
                "m/s",
                "yd/s",
                "ft/s",
            ]
        )

        self.distance_unit_combo = QComboBox()
        self.distance_unit_combo.addItems(
            ["miles", "kilometers", "meters", "yards", "feet"]
        )

        # Layout setup
        input_group = QGroupBox("Input Parameters")
        input_layout = QFormLayout(input_group)
        input_layout.addRow("Drone speed:", self.drone_speed)
        input_layout.addRow("Speed units:", self.speed_unit_combo)
        input_layout.addRow("Radar range:", self.radar_range)
        input_layout.addRow("Distance units:", self.distance_unit_combo)
        input_layout.addRow("Reaction time (min):", self.reaction_time)
        layout.addWidget(input_group)

        # Set default values
        self.drone_speed.setValue(30)
        self.radar_range.setValue(2)
        self.reaction_time.setValue(5)
        self.speed_unit_combo.setCurrentIndex(0)
        self.distance_unit_combo.setCurrentIndex(0)

        # Signals and slots
        self.drone_speed.valueChanged.connect(self.log_drone_speed)
        self.radar_range.valueChanged.connect(self.log_radar_range)
        self.reaction_time.valueChanged.connect(self.log_reaction_time)
        self.speed_unit_combo.currentIndexChanged.connect(self.log_speed_unit)
        self.distance_unit_combo.currentIndexChanged.connect(self.log_distance_unit)
        
        self.drone_speed.valueChanged.connect(self.validate_and_calculate)
        self.radar_range.valueChanged.connect(self.validate_and_calculate)
        self.reaction_time.valueChanged.connect(self.validate_and_calculate)
        self.speed_unit_combo.currentIndexChanged.connect(self.update_units)
        self.distance_unit_combo.currentIndexChanged.connect(self.update_units)
    
    def log_drone_speed(self):
        """
        Logs the value of the drone speed when it changes.
        """
        logging.debug(f"\nDrone speed changed to {self.drone_speed.value()}")
        
    def log_radar_range(self):
        """
        Logs the value of the radar range when it changes.
        """
        logging.debug(f"\nRadar range changed to {self.radar_range.value()}")
        
    def log_reaction_time(self):
        """
        Logs the value of the reaction time when it changes.
        """
        logging.debug(f"\nReaction time changed to {self.reaction_time.value()}")

    def log_distance_unit(self):
        """
        Logs the value of the distance unit when it changes.
        """
        logging.debug(f"\nDistance unit changed to {self.distance_unit_combo.currentText()}")

    def log_speed_unit(self):
        """
        Logs the value of the speed unit when it changes.
        """
        logging.debug(f"\nSpeed unit changed to {self.speed_unit_combo.currentText()}")

    def create_problem_group(self, layout):
        """
        Create the problem group with the problem statement and a button to start the simulation

        Parameters:
            layout (QVBoxLayout): The layout to add the problem group box to.
        """
        # Problem statement
        radar_range = str(self.radar_range.value())
        drone_speed = str(self.drone_speed.value())
        reaction_time = str(self.reaction_time.value())
        distance_unit = self.distance_unit_combo.currentText()
        speed_unit = self.speed_unit_combo.currentText()

        problem = (
            f"Radar intercept capability is {radar_range} {distance_unit}.\n"
            f"Drones (bad guys = them, good guys = us) both travel at  {drone_speed} {speed_unit}.\n"
            f"It takes us {reaction_time} minutes to react and get our drone up in the air.\n"
            "How far away do we intercept the drone?\n"
            "If we can't, what can we adjust?\n"
        )

        self.problem_label = QLabel(problem)

        # Layout setup
        problem_group = QGroupBox("Drone intercept problem")
        problem_layout = QVBoxLayout(problem_group)
        problem_layout.addWidget(self.problem_label)
        layout.addWidget(problem_group)

    def create_result_group(self, layout):
        """
        Create the result group with labels for the result and drone speed

        Parameters:
            layout (QVBoxLayout): The layout to add the result group box to.
        """
        # Result labels
        self.result_label = QLabel("Result will be shown here")
        self.drone_speed_label = QLabel("Drone speed (mph):")
        self.delay_distance_label = QLabel("Bad drone distance during delay:")
        self.suggestion_label = QLabel("Suggestions:")

        # Layout setup
        result_group = QGroupBox("Results")
        result_layout = QVBoxLayout(result_group)
        result_layout.addWidget(self.result_label)
        result_layout.addWidget(self.drone_speed_label)
        result_layout.addWidget(self.delay_distance_label)
        result_layout.addWidget(self.suggestion_label)
        layout.addWidget(result_group)

    def validate_and_calculate(self):
        """
        Validate the input fields and calculate the intercept distance
        """
        logging.debug("validate_and_calculate called")

        if not self.validate_input(self.drone_speed.value(), min_value=0):
            QMessageBox.warning(
                self, "Invalid Input", "Drone speed must be non-negative."
            )
            return
        if not self.validate_input(self.radar_range.value(), min_value=0):
            QMessageBox.warning(
                self, "Invalid Input", "Radar range must be non-negative."
            )
            return
        if not self.validate_input(self.reaction_time.value(), min_value=0):
            QMessageBox.warning(
                self, "Invalid Input", "Reaction time must be non-negative."
            )
            return
        self.calculate()

    def calculate(self):
        """
        Calculate the intercept distance and update the result labels
        """
        logging.debug("calculate called")

        speed_unit = self.speed_unit_combo.currentText()
        distance_unit = self.distance_unit_combo.currentText()

        # Calculate drone speed in miles per hour
        drone_speed_mph = UnitConverter.to_miles_per_hour(
            self.drone_speed.value(), speed_unit
        )

        # Calculate radar range in miles
        radar_range_miles = UnitConverter.to_miles(
            self.radar_range.value(), distance_unit
        )

        # Calculate intercept distance
        mins_drone_speed = drone_speed_mph / 60
        self.drone_speed_label.setText(f"Drone speed (mph): {drone_speed_mph:.4f}")

        miles_delay_distance = mins_drone_speed * self.reaction_time.value()
        delay_distance = UnitConverter.from_miles_to_unit(
            miles_delay_distance, distance_unit
        )
        self.delay_distance_label.setText(
            f"Bad drone distance during delay ({distance_unit}): {delay_distance:.4f}"
        )

        intercept_distance = (radar_range_miles - miles_delay_distance) / 2
        intercept_time = (
            intercept_distance / mins_drone_speed
        ) + self.reaction_time.value()
        intercept_possible = miles_delay_distance < radar_range_miles

        if intercept_possible:
            results = [f"We intercept the drone."]
            results.append(
                f"Interception distance: {intercept_distance:.2f} miles away"
            )
            results.append(f"Interception time: {intercept_time:.2f} minutes")
            self.result_label.setText("\n".join(results))
            self.suggestion_label.setText("")
        else:
            suggestions = self.generate_suggestions(
                drone_speed_mph, intercept_distance, distance_unit
            )
            self.result_label.setText("We can't intercept the drone")
            self.suggestion_label.setText("\n".join(suggestions))

        # Update the chart
        self.update_chart(
            mins_drone_speed,
            intercept_time,
            intercept_possible,
            distance_unit,
        )

        # Update the problem statement
        radar_range = str(self.radar_range.value())
        drone_speed = str(self.drone_speed.value())
        reaction_time = str(self.reaction_time.value())
        distance_unit = self.distance_unit_combo.currentText()
        speed_unit = self.speed_unit_combo.currentText()

        problem = (
            f"Radar intercept capability is {radar_range} {distance_unit}.\n"
            f"Drones (bad guys = them, good guys = us) both travel at  {drone_speed} {speed_unit}.\n"
            f"It takes us {reaction_time} minutes to react and get our drone up in the air.\n"
            "How far away do we intercept the drone?\n"
            "If we can't, what can we adjust?\n"
        )

        self.problem_label.setText(problem)

    def generate_suggestions(self, drone_speed_mph, intercept_distance, distance_unit):
        """
        Generate suggestions for intercepting the drone

        Parameters:
            drone_speed_mph (float): The drone speed in miles per hour.
            intercept_distance (float): The calculated intercept distance in miles.
            distance_unit (str): The unit of distance used for the suggestions (e.g., "miles", "km").

        Returns:
            list: A list of suggestions for intercepting the drone.
        """
        logging.debug("generate_suggestions called")

        suggestions = ["Suggestions:"]

        # Decrease drone speed
        required_drone_speed = (
            self.radar_range.value() / self.reaction_time.value()
        ) * 60
        suggestions.append(
            f"Decrease drone speed to less than {required_drone_speed:.2f} {self.speed_unit_combo.currentText()}"
        )

        # Decrease reaction time
        required_reaction_time = self.radar_range.value() / (drone_speed_mph / 60)
        suggestions.append(
            f"Decrease reaction time to less than {required_reaction_time:.2f} minutes"
        )

        # Increase radar range
        required_radar_range = UnitConverter.from_miles_to_unit(
            abs(intercept_distance), distance_unit
        )
        suggestions.append(
            f"Increase radar range to more than {required_radar_range:.2f} {distance_unit}"
        )

        return suggestions

    def update_chart(
        self,
        mins_drone_speed,
        intercept_time,
        intercept_possible,
        distance_unit,
    ):
        """
        Update the chart with the new intercept distance

        Parameters:
            mins_drone_speed (float): The drone speed in miles per minute.
            intercept_distance (float): The calculated intercept distance in miles.
            intercept_possible (bool): True if interception is possible, False otherwise.
            distance_unit (str): The unit of distance used for the chart (e.g., "miles", "km").
        """
        logging.debug("update_chart called")

        chart = QChart()
        chart.setTitle("Drone Intercept Visualization")
        max_time = max(
            self.reaction_time.value() * 2,
            self.radar_range.value() * 2 / mins_drone_speed,
        )

        # Series for radar range
        radar_series = QLineSeries()
        radar_series.setName("Radar Range")
        radar_series.append(0, self.radar_range.value())
        radar_series.append(max_time, self.radar_range.value())

        # Series for drone position
        drone_series = QLineSeries()
        drone_series.setName("Drone Position")
        drone_series.append(0, 0)
        drone_series.append(max_time, max_time * mins_drone_speed)
        max_distance = max(self.radar_range.value(), mins_drone_speed * max_time)

        # Intersect point
        intersect_series = QLineSeries()
        intersect_series.setName("Intersect Point")
        intersect_series.append(intercept_time, self.radar_range.value())
        intersect_series.append(intercept_time, 0)

        # Intercept point
        intercept_series = QScatterSeries()
        intercept_series.setName("Intercept Point")
        intercept_series.append(intercept_time, self.radar_range.value())

        # Set colors based on intercept possibility
        radar_series.setPen(
            QPen(QColor(Qt.cyan) if intercept_possible else QColor(Qt.magenta))
        )
        drone_series.setPen(
            QPen(QColor(Qt.blue) if intercept_possible else QColor(Qt.red))
        )
        intersect_series.setPen(QPen(QColor(Qt.darkGreen), 2, Qt.DashLine))
        intercept_series.setPen(QPen(QColor(Qt.darkGreen), 2, Qt.DashLine))
        if intercept_possible:
            intersect_series.setPen(QPen(QColor(Qt.green), 3))
            intercept_series.setPen(QPen(QColor(Qt.green), 3))
            intercept_series.setMarkerSize(15)

        chart.addSeries(radar_series)
        chart.addSeries(drone_series)
        chart.addSeries(intersect_series)
        chart.addSeries(intercept_series)

        # Create and configure x-axis
        axis_x = QValueAxis()
        axis_x.setTitleText("Time (minutes)")
        axis_x.setRange(0, max_time)
        axis_x.setTickCount(10)
        axis_x.setGridLineVisible(True)

        # Create and configure y-axis
        axis_y = QValueAxis()
        axis_y.setTitleText(f"Distance ({distance_unit})")
        axis_y.setRange(0, max_distance)
        axis_y.setTickCount(10)
        axis_y.setGridLineVisible(True)

        # Add axes to the chart
        chart.addAxis(axis_x, Qt.AlignBottom)
        chart.addAxis(axis_y, Qt.AlignLeft)

        # Attach series to the axes
        radar_series.attachAxis(axis_x)
        radar_series.attachAxis(axis_y)
        drone_series.attachAxis(axis_x)
        drone_series.attachAxis(axis_y)
        intersect_series.attachAxis(axis_x)
        intersect_series.attachAxis(axis_y)
        intercept_series.attachAxis(axis_x)
        intercept_series.attachAxis(axis_y)

        self.chart_view.setChart(chart)

    def update_units(self):
        """
        Update the units of the input fields and result labels
        """
        logging.debug("update_units called")

        self.calculate()

    def reset_to_default(self):
        """
        Reset input fields to default values
        """
        logging.debug("reset_to_default called")

        # Reset input fields
        self.drone_speed.setValue(30)
        self.radar_range.setValue(2)
        self.reaction_time.setValue(5)
        self.speed_unit_combo.setCurrentIndex(0)
        self.distance_unit_combo.setCurrentIndex(0)
        self.calculate()

    def start_simulation(self):
        """
        Start the drone intercept simulation
        """
        logging.debug("start_simulation called")

        # Get current values
        speed_unit = self.speed_unit_combo.currentText()
        distance_unit = self.distance_unit_combo.currentText()
        drone_speed_mph = UnitConverter.to_miles_per_hour(
            self.drone_speed.value(), speed_unit
        )
        radar_range_miles = UnitConverter.to_miles(
            self.radar_range.value(), distance_unit
        )

        # Create and show simulation window
        self.sim_window = DroneInterceptSimulation(
            drone_speed_mph, radar_range_miles, self.reaction_time.value()
        )
        self.sim_window.show()
