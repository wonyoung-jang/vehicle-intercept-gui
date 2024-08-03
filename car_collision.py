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
from car_collision_simulation import CarCollisionSimulation
from simulation_window import SimulationWindow
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


class CarCollisionWindow(SimulationWindow):
    # Log initialization
    logging.info("CarCollisionWindow initialized")

    def __init__(self):
        """
        Initialize the window
        """
        super().__init__()

    def create_input_group(self, layout):
        """
        Create the input group with input fields for car speeds and initial distance
        """
        # Input fields
        self.speed_car_a = QDoubleSpinBox()
        self.speed_car_a.setRange(0.0, 999999.0)

        self.speed_car_b = QDoubleSpinBox()
        self.speed_car_b.setRange(0.0, 999999.0)

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

        self.initial_distance = QDoubleSpinBox()
        self.initial_distance.setRange(0, 999999.0)

        self.distance_unit_combo = QComboBox()
        self.distance_unit_combo.addItems(
            ["miles", "kilometers", "meters", "yards", "feet"]
        )

        # Layout setup
        input_group = QGroupBox("Input Parameters")
        input_layout = QFormLayout(input_group)
        input_layout.addRow("Car A speed:", self.speed_car_a)
        input_layout.addRow("Car B speed:", self.speed_car_b)
        input_layout.addRow("Speed units:", self.speed_unit_combo)
        input_layout.addRow("Initial distance:", self.initial_distance)
        input_layout.addRow("Distance units:", self.distance_unit_combo)
        layout.addWidget(input_group)

        # Set default values
        self.speed_car_a.setValue(45)
        self.speed_car_b.setValue(27)
        self.speed_unit_combo.setCurrentIndex(0)
        self.initial_distance.setValue(200)
        self.distance_unit_combo.setCurrentIndex(4)

        # Signals and slots
        self.speed_car_a.valueChanged.connect(self.log_car_speed_a)
        self.speed_car_b.valueChanged.connect(self.log_car_speed_a)
        self.initial_distance.valueChanged.connect(self.log_initial_distance)
        self.distance_unit_combo.currentIndexChanged.connect(self.log_distance_unit)
        self.speed_unit_combo.currentIndexChanged.connect(self.log_speed_unit)
        
        self.speed_car_a.valueChanged.connect(self.validate_and_calculate)
        self.speed_car_b.valueChanged.connect(self.validate_and_calculate)
        self.initial_distance.valueChanged.connect(self.validate_and_calculate)
        self.distance_unit_combo.currentIndexChanged.connect(self.update_units)
        self.speed_unit_combo.currentIndexChanged.connect(self.update_units)

    def log_car_speed_a(self):
        """
        Logs the value of Car A's speed when it changes.
        """
        logging.debug(f"\nCar A speed changed to {self.speed_car_a.value()}")

    def log_initial_distance(self):
        """
        Logs the value of the initial distance when it changes.
        """
        logging.debug(f"\nInitial distance changed to {self.initial_distance.value()}")
        
    def log_car_speed_b(self):
        """
        Logs the value of Car B's speed when it changes.
        """
        logging.debug(f"\nCar B speed changed to {self.speed_car_b.value()}")
        
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
        car_a_speed = str(self.speed_car_a.value())
        car_b_speed = str(self.speed_car_b.value())
        initial_distance = str(self.initial_distance.value())
        distance_unit = self.distance_unit_combo.currentText()
        speed_unit = self.speed_unit_combo.currentText()

        problem = (
            f"Car A is traveling {car_a_speed} {speed_unit}.\n"
            f"Car B is traveling {car_b_speed} {speed_unit}.\n"
            f"Car B is traveling in the same lane {initial_distance} {distance_unit} in front of Car A.\n"
            "How long until the cars collide?"
        )

        self.problem_label = QLabel(problem)

        # Layout setup
        problem_group = QGroupBox("Car collision problem")
        problem_layout = QVBoxLayout(problem_group)
        problem_layout.addWidget(self.problem_label)
        layout.addWidget(problem_group)

    def create_result_group(self, layout):
        """
        Create the group for displaying the result

        Parameters:
            layout (QVBoxLayout): The layout to add the result group box to.
        """
        # Result label
        self.result_label = QLabel("Result will be shown here")

        # Layout setup
        result_group = QGroupBox("Results")
        result_layout = QVBoxLayout(result_group)
        result_layout.addWidget(self.result_label)
        layout.addWidget(result_group)

    def validate_and_calculate(self):
        """
        Validate the input values and calculate the time to collision
        """
        logging.debug("validate_and_calculate called")

        if not self.validate_input(self.speed_car_a.value(), min_value=0):
            QMessageBox.warning(
                self, "Invalid Input", "Car A speed must be non-negative."
            )
            return
        if not self.validate_input(self.speed_car_b.value(), min_value=0):
            QMessageBox.warning(
                self, "Invalid Input", "Car B speed must be non-negative."
            )
            return
        if not self.validate_input(self.initial_distance.value(), min_value=0):
            QMessageBox.warning(
                self, "Invalid Input", "Initial distance must be non-negative."
            )
            return
        self.calculate()

    def calculate(self):
        """
        Calculate the time to collision and update the result label
        """
        logging.debug("calculate called")

        speed_unit = self.speed_unit_combo.currentText()
        distance_unit = self.distance_unit_combo.currentText()

        # Calculate the speed of car A in miles per hour
        speed_car_a_mph = UnitConverter.to_miles_per_hour(
            self.speed_car_a.value(), speed_unit
        )

        # Calculate the speed of car B in miles per hour
        speed_car_b_mph = UnitConverter.to_miles_per_hour(
            self.speed_car_b.value(), speed_unit
        )

        # Calculate the initial distance between the cars in miles
        initial_distance_miles = UnitConverter.to_miles(
            self.initial_distance.value(), distance_unit
        )

        # Calculate the relative speed of the cars
        speed_difference = speed_car_a_mph - speed_car_b_mph

        if speed_difference <= 0:
            self.result_label.setText("The cars will never collide.")
            self.update_chart(0, distance_unit)
            return

        # Calculate time to collision in hours
        time_to_collision_hours = initial_distance_miles / speed_difference

        # Convert time to minutes and seconds
        total_seconds = time_to_collision_hours * 3600
        minutes = int(total_seconds // 60)
        seconds = int(total_seconds % 60)
        milliseconds = int((total_seconds % 1) * 1000)

        self.result_label.setText(
            f"The cars will collide in {minutes} minutes and {seconds}.{milliseconds} seconds."
        )

        # Update the problem statement
        car_a_speed = str(self.speed_car_a.value())
        car_b_speed = str(self.speed_car_b.value())
        initial_distance = str(self.initial_distance.value())
        distance_unit = self.distance_unit_combo.currentText()
        speed_unit = self.speed_unit_combo.currentText()

        problem = (
            f"Car A is traveling {car_a_speed} {speed_unit}.\n"
            f"Car B is traveling {car_b_speed} {speed_unit}.\n"
            f"Car B is traveling in the same lane {initial_distance} {distance_unit} in front of Car A.\n"
            "How long until the cars collide?"
        )

        self.problem_label.setText(problem)

        # Update the chart
        self.update_chart(time_to_collision_hours, distance_unit)

    def update_chart(self, time_to_collision, distance_unit):
        """
        Update the chart with the new time to collision

        Parameters:
            time_to_collision (float): The calculated time to collision in hours.
            distance_unit (str): The unit of distance used for the chart (e.g., "miles", "km").
        """
        logging.debug("update_chart called")

        # Calculate the maximum time for the chart
        max_time = time_to_collision * 1.5 if time_to_collision > 0 else 1

        # Convert speeds to the chart's distance unit per hour
        speed_car_a = UnitConverter.from_miles_to_unit(
            UnitConverter.to_miles_per_hour(
                self.speed_car_a.value(), self.speed_unit_combo.currentText()
            ),
            distance_unit,
        )

        # Convert speeds to the chart's distance unit per hour
        speed_car_b = UnitConverter.from_miles_to_unit(
            UnitConverter.to_miles_per_hour(
                self.speed_car_b.value(), self.speed_unit_combo.currentText()
            ),
            distance_unit,
        )

        # Convert initial distance to the chart's distance unit
        initial_distance = UnitConverter.from_miles_to_unit(
            UnitConverter.to_miles(
                self.initial_distance.value(), self.distance_unit_combo.currentText()
            ),
            distance_unit,
        )

        # Series for Car A
        series_a = QLineSeries()
        series_a.setName("Car A")
        series_a.append(0, 0)
        series_a.append(max_time, speed_car_a * max_time)

        # Series for Car B
        series_b = QLineSeries()
        series_b.setName("Car B")
        series_b.append(0, initial_distance)
        series_b.append(max_time, initial_distance + speed_car_b * max_time)

        # Calculate max distance for y-axis
        max_distance = max(
            speed_car_a * max_time, initial_distance + speed_car_b * max_time
        )

        # Intersect point
        intersect_series = QLineSeries()
        intersect_series.setName("Intersect Point")
        intersect_series.append(0, speed_car_a * time_to_collision)
        intersect_series.append(time_to_collision, speed_car_a * time_to_collision)
        intersect_series.append(time_to_collision, 0)

        # Collision point
        collision_series = QScatterSeries()
        collision_series.setName("Collision Point")
        if time_to_collision > 0:
            collision_point = speed_car_a * time_to_collision
            collision_series.append(time_to_collision, collision_point)

        # Set colors
        series_a.setPen(QPen(QColor(Qt.blue), 2))
        series_b.setPen(QPen(QColor(Qt.red), 2))
        intersect_series.setPen(QPen(QColor(Qt.green), 2, Qt.DashLine))
        collision_series.setColor(QColor(Qt.green))
        collision_series.setMarkerSize(15)

        # Create and configure x-axis
        axis_x = QValueAxis()
        axis_x.setTitleText("Time (hours)")
        axis_x.setRange(0, max_time)
        axis_x.setTickCount(10)
        axis_x.setGridLineVisible(True)

        # Create and configure y-axis
        axis_y = QValueAxis()
        axis_y.setTitleText(f"Distance ({distance_unit})")
        axis_y.setRange(0, max_distance)
        axis_y.setTickCount(10)
        axis_y.setGridLineVisible(True)

        # Chart setup
        chart = QChart()
        chart.setTitle("Car Collision Visualization")

        chart.addSeries(intersect_series)
        chart.addSeries(series_a)
        chart.addSeries(series_b)
        chart.addSeries(collision_series)

        chart.addAxis(axis_x, Qt.AlignBottom)
        chart.addAxis(axis_y, Qt.AlignLeft)

        # Attach series to the axes
        series_a.attachAxis(axis_x)
        series_a.attachAxis(axis_y)
        series_b.attachAxis(axis_x)
        series_b.attachAxis(axis_y)
        intersect_series.attachAxis(axis_x)
        intersect_series.attachAxis(axis_y)
        collision_series.attachAxis(axis_x)
        collision_series.attachAxis(axis_y)

        # Set chart to view
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
        self.speed_car_a.setValue(45)
        self.speed_car_b.setValue(27)
        self.initial_distance.setValue(200)
        self.speed_unit_combo.setCurrentIndex(0)
        self.distance_unit_combo.setCurrentIndex(4)
        self.calculate()

    def start_simulation(self):
        """
        Start the car collision simulation
        """
        logging.debug("start_simulation called")

        # Get current values
        speed_unit = self.speed_unit_combo.currentText()
        distance_unit = self.distance_unit_combo.currentText()
        speed_car_a_mph = UnitConverter.to_miles_per_hour(
            self.speed_car_a.value(), speed_unit
        )
        speed_car_b_mph = UnitConverter.to_miles_per_hour(
            self.speed_car_b.value(), speed_unit
        )
        initial_distance_miles = UnitConverter.to_miles(
            self.initial_distance.value(), distance_unit
        )

        # Create and show simulation window
        self.sim_window = CarCollisionSimulation(
            speed_car_a_mph, speed_car_b_mph, initial_distance_miles
        )
        self.sim_window.show()
